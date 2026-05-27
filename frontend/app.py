# ---------------- app.py ----------------
import streamlit as st
import sqlite3
import os
import math
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Generative AI Virtual STEM Lab")

# ---------------- PATHS ----------------
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "lab.db")
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")

# -------------
# --- DATABASE ----------------
def get_conn():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE,
        password TEXT,
        class_group TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS report(
        student TEXT,
        experiment TEXT,
        score INTEGER
    )
    """)
    conn.commit()
    conn.close()

def register_student(roll_no, password, class_group):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students(roll_no,password,class_group) VALUES(?,?,?)",
            (roll_no,password,class_group)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_student(roll_no, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT roll_no,class_group FROM students WHERE roll_no=? AND password=?",
        (roll_no,password)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {"roll_no":row[0],"class_group":row[1]}
    return None

create_tables()

# ---------------- PERFORMANCE ----------------
def save_attempt(student, experiment, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO report(student, experiment, score) VALUES (?,?,?)", (student, experiment, score))
    conn.commit()
    conn.close()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None
if "hint_level" not in st.session_state:
    st.session_state.hint_level = 0

# ---------------- LOGIN / REGISTER ----------------
st.title("🧪 Adaptive Generative AI Tutor For STEM Labs")

if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Login","Register"])

    with tab1:
        st.subheader("Student Login")
        roll = st.text_input("Roll Number", key="login_roll")
        pwd = st.text_input("Password", type="password", key="login_pwd")

        if st.button("Login"):
            user = login_student(roll,pwd)
            if user:
                st.session_state.user = user
                st.success("Login successful")
                st.stop()
            else:
                st.error("Invalid Roll Number or Password")

    with tab2:
        st.subheader("Student Registration")
        r = st.text_input("Roll Number", key="reg_roll")
        p = st.text_input("Password", type="password", key="reg_pwd")
        cls = st.selectbox("Class Group", ["9-10","11-12"])

        if st.button("Register"):
            ok = register_student(r,p,cls)
            if ok:
                st.success("Registered successfully! Now login.")
            else:
                st.error("Roll number already exists")

    st.stop()

# ---------------- AFTER LOGIN ----------------
st.sidebar.success(f"Logged in as: {st.session_state.user['roll_no']}")
group = st.session_state.user["class_group"]

if group=="9-10":
    subjects=["Science-1","Science-2"]
else:
    subjects=["Physics","Chemistry","Biology"]

subject=st.selectbox("Select Subject",subjects)

# ---------------- UTILITY ----------------
def show_image(name):
    path = os.path.join(IMAGE_DIR, name)
    if os.path.exists(path):
        st.image(path, width=400)
    else:
        st.warning(f"Image {name} not found!")

def check_answer(real, student, tol=0.5):
    try:
        return abs(real - float(student)) <= tol
    except:
        return False

# ---------------- INTERACTIVE PLOTS ----------------
def plot_reflection(values):
    angle = values["angle"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0,1], y=[0,math.tan(math.radians(angle))], mode="lines+markers", name="Incident Ray"))
    fig.add_trace(go.Scatter(x=[1,2], y=[math.tan(math.radians(angle)),math.tan(math.radians(angle))], mode="lines+markers", name="Reflected Ray"))
    fig.update_layout(width=400, height=300, title="Reflection Ray Diagram", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig)

def plot_projectile(values):
    v = values["v"]
    angle = math.radians(values["angle"])
    t_flight = 2*v*math.sin(angle)/9.8
    t = [i*t_flight/50 for i in range(51)]
    x = [v*math.cos(angle)*ti for ti in t]
    y = [v*math.sin(angle)*ti - 0.5*9.8*ti**2 for ti in t]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="Projectile Path"))
    fig.update_layout(width=500, height=300, title="Projectile Trajectory", xaxis_title="X (m)", yaxis_title="Y (m)")
    st.plotly_chart(fig)

def plot_pendulum(values):
    L = values["length"]
    T = 2*math.pi*math.sqrt(L/9.8)
    times = [i*0.1 for i in range(21)]
    theta = [math.radians(30)*math.cos(2*math.pi*t/T) for t in times]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=theta, mode="lines+markers", name="Pendulum"))
    fig.update_layout(width=500, height=300, title="Pendulum Oscillation", xaxis_title="Time (s)", yaxis_title="Angle (rad)")
    st.plotly_chart(fig)
import time

def simulate_projectile(values):
    v = values["v"]          # ✅ correct key
    angle = math.radians(values["angle"])
    g = 9.8

    if "run_proj" not in st.session_state:
        st.session_state.run_proj = False
    if "t_proj" not in st.session_state:
        st.session_state.t_proj = 0.0

    t_flight = 2 * v * math.sin(angle) / g
    dt = t_flight / 40 if t_flight > 0 else 0.1

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ PLAY", key="play_proj"):
            st.session_state.run_proj = True
    with col2:
        if st.button("⏹ RESET", key="reset_proj"):
            st.session_state.run_proj = False
            st.session_state.t_proj = 0.0

    placeholder = st.empty()
    info_box = st.empty()

    if st.session_state.run_proj:
        t = st.session_state.t_proj

        x = v * math.cos(angle) * t
        y = v * math.sin(angle) * t - 0.5 * g * t**2

        if y < 0:
            y = 0
            st.session_state.run_proj = False

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0, x], y=[0, y],
            mode="lines+markers",
            marker=dict(size=10)
        ))

        fig.update_layout(
            title="Projectile in Motion",
            xaxis_title="Distance (m)",
            yaxis_title="Height (m)",
            xaxis=dict(range=[0, max(5, x+2)]),
            yaxis=dict(range=[0, max(5, y+2)]),
            height=350
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        info_box.markdown(
            f"**Time:** {t:.2f}s | **X:** {x:.2f} m | **Y:** {y:.2f} m"
        )

        st.session_state.t_proj += dt
        time.sleep(0.05)
        st.rerun()

def simulate_pendulum(values):
    L = values["L"]   
    g = 9.8
    T = 2 * math.pi * math.sqrt(L / g)
    theta0 = math.radians(30)
    dt = 0.05

    if "run_pend" not in st.session_state:
        st.session_state.run_pend = False
    if "t_pend" not in st.session_state:
        st.session_state.t_pend = 0.0

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ PLAY", key="play_pend"):
            st.session_state.run_pend = True
    with col2:
        if st.button("⏹ RESET", key="reset_pend"):
            st.session_state.run_pend = False
            st.session_state.t_pend = 0.0

    placeholder = st.empty()
    info_box = st.empty()

    if st.session_state.run_pend:
        t = st.session_state.t_pend
        theta = theta0 * math.cos(2 * math.pi * t / T)
        x = L * math.sin(theta)
        y = -L * math.cos(theta)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0, x], y=[0, y],
            mode="lines+markers",
            marker=dict(size=12)
        ))
        fig.update_layout(
            title="Pendulum in Motion",
            xaxis=dict(range=[-L, L]),
            yaxis=dict(range=[-L, 0.2]),
            height=350
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        info_box.markdown(f"**Time:** {t:.2f}s | **Angle:** {math.degrees(theta):.1f}°")

        st.session_state.t_pend += dt
        time.sleep(dt)
        st.rerun()
def simulate_hooke(values):
    k = values["k"]
    x_max = values["x"]

    mass = 1.0
    g = 9.8
    omega = math.sqrt(k / mass)

    placeholder = st.empty()
    t = 0
    dt = 0.1

    xs, ys = [], []

    while t <= 10:
        x = x_max * math.cos(omega * t)
        y = -x

        xs.append(0)
        ys.append(y)

        fig = go.Figure()

        # spring (line)
        fig.add_trace(go.Scatter(
            x=[0, 0],
            y=[0, y],
            mode="lines",
            line=dict(width=4),
            name="Spring"
        ))

        # mass (circle)
        fig.add_trace(go.Scatter(
            x=[0],
            y=[y],
            mode="markers",
            marker=dict(size=20),
            name="Mass"
        ))

        force = k * abs(x)

        fig.update_layout(
            title=f"Spring Motion | Force = {force:.2f} N",
            xaxis=dict(range=[-1, 1]),
            yaxis=dict(range=[-x_max*2, x_max*2]),
            height=400,
            showlegend=False
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)
        t += dt
# ---------------- EXPERIMENT DATA ----------------
# Top 15 enhanced + remaining 10 simple
experiments_by_subject = {
    "Science-1": {
        "Reflection": {
            "title":"Law of Reflection",
            "apparatus":["Plane Mirror","Protractor","Laser pointer"],
            "procedure":["Place mirror flat","Shine laser at an angle","Measure incidence and reflection angles"],
            "params":[{"name":"angle","label":"Angle of incidence (°)","min":10,"max":80,"default":30}],
            "formula":lambda v:v["angle"],
            "hints":["Angle of incidence equals angle of reflection","Measure from normal"],
            "observation":"Observe how reflected angle equals incident angle.",
            "img":"reflection.png",
            "interactive_plot": plot_reflection
        },
        "Ohm": {
            "title":"Ohm's Law",
            "apparatus":["Resistor","Battery","Ammeter","Voltmeter"],
            "procedure":["Connect resistor to battery","Measure voltage and current","Vary voltage to see current change"],
            "params":[{"name":"V","label":"Voltage (V)","min":1,"max":20,"default":5},
                      {"name":"R","label":"Resistance (Ω)","min":1,"max":50,"default":10}],
            "formula":lambda v:v["V"]/v["R"],
            "hints":["I ∝ V","I = V/R","Observe change when R changes"],
            "observation":"Current changes proportionally with voltage.",
            "img":"ohms_law.png"
        },
        "Density": {
            "title":"Density Measurement",
            "apparatus":["Block","Balance","Ruler"],
            "procedure":["Measure mass of block","Measure volume","Compute density"],
            "params":[{"name":"mass","label":"Mass (g)","min":50,"max":500,"default":100},
                      {"name":"volume","label":"Volume (cm³)","min":10,"max":200,"default":20}],
            "formula":lambda v:v["mass"]/v["volume"],
            "hints":["Density = mass/volume","Divide mass by volume"],
            "observation":"See how mass and volume affect density.",
            "img":"density_block.png"
        },
        "Pendulum": {
            "title":"Simple Pendulum",
            "apparatus":["String","Bob","Stopwatch"],
            "procedure":["Fix bob to string","Measure length","Time oscillations"],
            "params":[{"name":"length","label":"Length (m)","min":0.5,"max":2.0,"default":1.0}],
            "formula":lambda v:2*math.pi*math.sqrt(v["length"]/9.8),
            "hints":["T = 2π√(L/g)","Longer length → longer period"],
            "observation":"Observe oscillation time with length.",
            "img":"pendulum.png",
            "interactive_plot": plot_pendulum
        },
        "Heat Conduction": {
            "title":"Heat Conduction",
            "apparatus":["Metal rod","Heat source","Thermometer"],
            "procedure":["Heat one end of rod","Measure temperature change","Observe conduction"],
            "params":[{"name":"hot","label":"Hot End Temp (°C)","min":50,"max":200,"default":100},
                      {"name":"cold","label":"Cold End Temp (°C)","min":20,"max":100,"default":30}],
            "formula":lambda v:(v["hot"]-v["cold"])*0.5,
            "hints":["Heat flows from hot to cold","Observe temperature change"],
            "observation":"Metal conducts heat from hot to cold end.",
            "img":"heat_conduction.png"
        }
    },
    "Science-2": {
        "Osmosis": {
            "title":"Osmosis in Plant Cells",
            "apparatus":["Potato slices","Salt solution","Beaker"],
            "procedure":["Place potato in solution","Observe water movement","Measure length change"],
            "params":[{"name":"conc","label":"Concentration (%)","min":1,"max":20,"default":5}],
            "formula":lambda v:20-v["conc"],
            "hints":["Water moves to higher solute concentration","Observe shrinkage or swelling"],
            "observation":"Potato slice changes size depending on solution.",
            "img":"osmosis.png"
        },
        "Photosynthesis": {
            "title":"Photosynthesis Rate",
            "apparatus":["Leaf","Light source","Iodine"],
            "procedure":["Expose leaf to light","Test for starch","Observe color change"],
            "params":[{"name":"light","label":"Light Intensity","min":1,"max":10,"default":5}],
            "formula":lambda v:v["light"]*2,
            "hints":["More light → more starch","Rate ∝ light intensity"],
            "observation":"Leaf produces more starch under strong light.",
            "img":"photosynthesis.png"
        },
        "Respiration": {
            "title":"Cellular Respiration",
            "apparatus":["Yeast","Sugar solution","Test tube"],
            "procedure":["Mix yeast and sugar","Observe gas evolution","Measure CO₂"],
            "params":[{"name":"oxygen","label":"Oxygen Level","min":1,"max":10,"default":5}],
            "formula":lambda v:v["oxygen"]*3,
            "hints":["More oxygen → more energy released"],
            "observation":"Energy release increases with oxygen.",
            "img":"respiration.png"
        },
        "Diffusion": {
            "title":"Diffusion Experiment",
            "apparatus":["Potassium permanganate","Water","Beaker"],
            "procedure":["Add crystal to water","Observe spread","Measure time taken"],
            "params":[{"name":"time","label":"Time (min)","min":1,"max":10,"default":5}],
            "formula":lambda v:10-v["time"],
            "hints":["Substance moves from high to low concentration"],
            "observation":"Diffusion happens gradually in water.",
            "img":"diffusion.png"
        },
        "Transpiration": {
            "title":"Transpiration Rate",
            "apparatus":["Leaf","Potometer","Water"],
            "procedure":["Set up potometer","Measure water loss","Observe effect of wind/light"],
            "params":[{"name":"humidity","label":"Humidity (%)","min":10,"max":90,"default":50}],
            "formula":lambda v:100-v["humidity"],
            "hints":["Lower humidity → higher transpiration"],
            "observation":"Water loss increases as humidity drops.",
            "img":"transpiration.png"
        }
    },
   "Physics": {
        "Projectile": {
        "title":"Projectile Motion",
        "apparatus":["Cannon","Measuring tape","Protractor"],
        "procedure":["Set angle and velocity","Observe path","Measure range"],
        "params":[
            {"name":"v","label":"Velocity (m/s)","min":5,"max":50,"default":20},
            {"name":"angle","label":"Angle (°)","min":10,"max":80,"default":45}
        ],
        "formula":lambda v:(v["v"]**2*math.sin(2*math.radians(v["angle"])))/9.8,
        "hints":["45° gives max range","Range ∝ velocity²"],
        "observation":"Projectile follows parabolic path.",
        "img":"projectile.png",
        "interactive_sim": simulate_projectile
    },

    "Pendulum": {
        "title":"Simple Pendulum",
        "apparatus":["String","Bob","Stopwatch"],
        "procedure":["Displace bob","Release","Observe oscillation"],
        "params":[
            {"name":"L","label":"Length (m)","min":0.5,"max":3.0,"default":1.0}
        ],
        "formula":lambda v:2*math.pi*math.sqrt(v["L"]/9.8),
        "hints":["Longer pendulum → more time period"],
        "observation":"Pendulum oscillates periodically.",
        "img":"pendulum.png",
        "interactive_sim": simulate_pendulum
    },

    "Hooke": {
        "title":"Hooke's Law",
        "apparatus":["Spring","Weight"],
        "procedure":["Apply force","Observe extension"],
        "params":[
            {"name":"k","label":"Spring constant (N/m)","min":10,"max":100,"default":20},
            {"name":"x","label":"Max Extension (m)","min":0.1,"max":1.0,"default":0.5}
        ],
        "formula":lambda v:v["k"]*v["x"],
        "hints":["F = kx"],
        "observation":"Force proportional to extension.",
        "img":"hooke.png",
        "interactive_sim": simulate_hooke
    },

    "Magnetic": {
        "title":"Magnetic Field",
        "apparatus":["Magnet","Compass","Iron filings"],
        "procedure":["Place magnet","Observe field lines","Use filings to visualize"],
        "params":[
            {"name":"I","label":"Current (A)","min":1,"max":10,"default":5}
        ],
        "formula":lambda v:v["I"]*2,
        "hints":["Field ∝ current","More current → stronger field"],
        "observation":"Magnetic field strength increases with current.",
        "img":"magnetic.png"
    },

    "Microscope": {
        "title":"Microscope Magnification",
        "apparatus":["Microscope","Slide","Lens"],
        "procedure":["Place slide","Adjust focus","Measure magnification"],
        "params":[
            {"name":"obj","label":"Objective Lens","min":1,"max":10,"default":5},
            {"name":"eye","label":"Eyepiece Lens","min":5,"max":20,"default":10}
        ],
        "formula":lambda v:v["obj"]*v["eye"],
        "hints":["Magnification = objective × eyepiece"],
        "observation":"Observe enlarged image of specimen.",
        "img":"microscope.png"
    },

    "Heat Neutral": {
        "title":"Heat of Neutralization",
        "apparatus":["Acid","Base","Calorimeter","Thermometer"],
        "procedure":["Mix acid and base","Measure temperature rise","Calculate heat released"],
        "params":[
            {"name":"v","label":"Volume (ml)","min":10,"max":50,"default":20}
        ],
        "formula":lambda v:v["v"]*4.2,
        "hints":["Exothermic reaction","ΔT ∝ heat released"],
        "observation":"Temperature rises after neutralization.",
        "img":"heat_neutralization.png"
    }
},
    
    "Chemistry": {
        "Titration": {
            "title":"Acid-Base Titration",
            "apparatus":["Burette","Acid","Base","Indicator"],
            "procedure":["Fill burette","Add base to acid","Observe color change"],
            "params":[{"name":"V","label":"Volume (ml)","min":10,"max":50,"default":25}],
            "formula":lambda v:v["V"]*0.1,
            "hints":["Neutralization occurs at endpoint"],
            "observation":"Color change indicates neutralization.",
            "img":"titration.png"
        },
        "Acid Base": {
            "title":"pH Measurement",
            "apparatus":["pH paper","Solution"],
            "procedure":["Dip pH paper","Compare color with chart","Record pH"],
            "params":[{"name":"pH","label":"Solution pH","min":1,"max":14,"default":7}],
            "formula":lambda v:14-v["pH"],
            "hints":["Acid pH<7, Base pH>7"],
            "observation":"pH tells acidity or basicity.",
            "img":"acid_base.png"
        },
        "Electrolysis Water": {
            "title":"Electrolysis of Water",
            "apparatus":["Electrolytic cell","Power supply","Water"],
            "procedure":["Pass current","Observe gas evolution","Collect H2 and O2"],
            "params":[{"name":"I","label":"Current (A)","min":1,"max":10,"default":3}],
            "formula":lambda v:v["I"]*2,
            "hints":["H2 at cathode, O2 at anode"],
            "observation":"Gas collected proportional to current.",
            "img":"electrolysis_water.png"
        },
        "Electrolysis Cu": {
            "title":"Electrolysis of Copper",
            "apparatus":["Copper electrodes","CuSO4 solution","Power supply"],
            "procedure":["Connect electrodes","Pass current","Observe mass change"],
            "params":[{"name":"t","label":"Time (min)","min":1,"max":60,"default":20}],
            "formula":lambda v:v["t"]*0.05,
            "hints":["Anode dissolves, cathode gains mass"],
            "observation":"Copper mass changes with time.",
            "img":"electrolysis_cu.png"
        },
        "Reaction Rate": {
            "title":"Reaction Rate",
            "apparatus":["Reagents","Timer","Beaker"],
            "procedure":["Mix reagents","Observe change","Measure time"],
            "params":[{"name":"temp","label":"Temperature (°C)","min":20,"max":80,"default":40}],
            "formula":lambda v:v["temp"]*1.5,
            "hints":["Higher temp → faster reaction"],
            "observation":"Reaction rate increases with temperature.",
            "img":"reaction_rate.png"
        }
    },
    "Biology": {
        "Enzyme": {
            "title":"Enzyme Activity",
            "apparatus":["Enzyme solution","Substrate","Test tubes"],
            "procedure":["Mix enzyme and substrate","Observe reaction","Measure rate"],
            "params":[{"name":"temp","label":"Temperature (°C)","min":0,"max":80,"default":30}],
            "formula":lambda v:-0.05*(v["temp"]-37)**2+50,
            "hints":["Optimal temp → max activity"],
            "observation":"Enzyme activity peaks at 37°C",
            "img":"enzyme.png"
        },
        "Respiration Bio": {
            "title":"Cellular Respiration",
            "apparatus":["Yeast","Glucose solution","Test tube"],
            "procedure":["Mix yeast and glucose","Observe gas","Measure energy release"],
            "params":[{"name":"oxygen","label":"Oxygen Level","min":1,"max":10,"default":5}],
            "formula":lambda v:v["oxygen"]*3,
            "hints":["More oxygen → more energy"],
            "observation":"Energy released increases with oxygen.",
            "img":"respiration.png"
        },
        "Heart": {
            "title":"Heart Rate Measurement",
            "apparatus":["Stethoscope","Stopwatch"],
            "procedure":["Measure pulse","Count beats","Calculate bpm"],
            "params":[{"name":"pulse","label":"Beats per Minute","min":60,"max":120,"default":80}],
            "formula":lambda v:v["pulse"]/2,
            "hints":["Observe heart rate changes"],
            "observation":"Heart rate responds to activity.",
            "img":"heart.png"
        },
        "Transpiration Bio": {
            "title":"Transpiration in Plants",
            "apparatus":["Leaf","Potometer","Water"],
            "procedure":["Set up leaf","Measure water loss","Observe stomata effect"],
            "params":[{"name":"humidity","label":"Humidity (%)","min":1,"max":10,"default":5}],
            "formula":lambda v:v["humidity"]*1.5,
            "hints":["Lower humidity → higher water loss"],
            "observation":"Transpiration increases in dry air.",
            "img":"transpiration.png"
        },
        "Microscope Bio": {
            "title":"Microscope Observation",
            "apparatus":["Microscope","Slide","Lens"],
            "procedure":["Place slide","Adjust focus","Observe specimen"],
            "params":[{"name":"obj","label":"Objective Lens","min":1,"max":10,"default":5},
                      {"name":"eye","label":"Eyepiece Lens","min":5,"max":20,"default":10}],
            "formula":lambda v:v["obj"]*v["eye"],
            "hints":["Magnification = objective × eyepiece"],
            "observation":"See enlarged image of cells.",
            "img":"microscope.png"
        }
    }
}

# ---------------- SELECT AND RUN EXP ----------------
# ---------------- RUN EXPERIMENT ----------------
experiment = st.selectbox("Select Experiment", list(experiments_by_subject[subject].keys()))
exp = experiments_by_subject[subject][experiment]

st.subheader(f"{exp['title']}")
st.markdown(f"**Apparatus:** {', '.join(exp['apparatus'])}")
st.markdown("**Procedure:**")
for step in exp['procedure']:
    st.markdown(f"- {step}")

col1, col2 = st.columns([2,1])
values = {}

with col1:
    if "params" in exp:
        for param in exp["params"]:
            values[param["name"]] = st.slider(param["label"], param["min"], param["max"], param["default"])
    show_image(exp.get("img",""))
    if "interactive_sim" in exp:
        exp["interactive_sim"](values)
    if st.button("🔄 Reset", key=f"reset_{experiment}"):
       st.rerun()
with col2:
    ans = st.text_input("Enter calculated result")
    if st.button("Check Answer"):
        real = exp["formula"](values)
        if check_answer(real, ans):
            st.success(f"Correct ✔. Expected value: {real:.2f}")
            st.session_state.hint_level = 0
            save_attempt(st.session_state.user["roll_no"], experiment, 1)
        else:
            st.session_state.hint_level +=1
            hints = exp.get("hints", [f"Expected ~{real:.2f}"])
            idx = min(st.session_state.hint_level - 1, len(hints) - 1)
            st.warning(f"Hint: {hints[idx]}")
            save_attempt(st.session_state.user["roll_no"], experiment, 0)

# ---------------- PERFORMANCE REPORT ----------------
if st.checkbox("Show My Performance Report"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT experiment,score FROM report WHERE student=?",(st.session_state.user["roll_no"],))
    rows = c.fetchall()
    conn.close()
    if rows:
        import pandas as pd
        df = pd.DataFrame(rows, columns=["Experiment","Score"])
        st.dataframe(df)
        st.download_button("Download Report CSV", df.to_csv(index=False).encode('utf-8'), "report.csv")
    else:
        st.info("No attempts recorded yet.")