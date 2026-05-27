import streamlit as st
import os
import math

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")

def show_image(name):
    path = os.path.join(IMAGE_DIR, name)
    if os.path.exists(path):
        st.image(path, use_column_width=True)
    else:
        st.error("Image not found: " + name)

def check_answer(real, student, tol=0.5):
    try:
        return abs(real - float(student)) <= tol
    except:
        return False

# ---------- SCIENCE 1 ----------
def exp_reflection():
    show_image("reflection.png")
    a = st.slider("Angle of incidence", 10, 80, 30)
    ans = st.text_input("Enter angle of reflection")
    if st.button("Check Answer"):
        ok = check_answer(a, ans)
        return ok, a
    return None, None

def exp_ohm():
    show_image("ohms_law.png")
    V = st.slider("Voltage", 1, 20, 5)
    R = st.slider("Resistance", 1, 50, 10)
    I = V / R
    ans = st.text_input("Enter current")
    if st.button("Check Answer"):
        ok = check_answer(I, ans)
        return ok, I
    return None, None

def exp_density():
    show_image("density_block.png")
    m = st.slider("Mass", 50, 500, 100)
    v = st.slider("Volume", 10, 200, 20)
    d = m / v
    ans = st.text_input("Enter density")
    if st.button("Check Answer"):
        ok = check_answer(d, ans)
        return ok, d
    return None, None

def exp_pendulum():
    show_image("pendulum.png")
    L = st.slider("Length", 0.5, 2.0, 1.0)
    T = 2*math.pi*math.sqrt(L/9.8)
    ans = st.text_input("Enter time period")
    if st.button("Check Answer"):
        ok = check_answer(T, ans)
        return ok, T
    return None, None

def exp_heat_conduction():
    show_image("heat_conduction.png")
    t1 = st.slider("Hot end temp",50,200,100)
    t2 = st.slider("Cold end temp",20,100,30)
    q = (t1-t2)*0.5
    ans = st.text_input("Enter heat flow")
    if st.button("Check Answer"):
        ok = check_answer(q, ans)
        return ok, q
    return None, None

# ---------- SCIENCE 2 ----------
def exp_osmosis():
    show_image("osmosis.png")
    c = st.slider("Concentration",0,20,5)
    ch = 20-c
    ans = st.text_input("Enter change")
    if st.button("Check Answer"):
        ok = check_answer(ch, ans)
        return ok, ch
    return None, None

def exp_photosynthesis():
    show_image("photosynthesis.png")
    l = st.slider("Light",1,10,5)
    r = l*2
    ans = st.text_input("Enter rate")
    if st.button("Check Answer"):
        ok = check_answer(r, ans)
        return ok, r
    return None, None

def exp_respiration():
    show_image("respiration.png")
    o = st.slider("Oxygen",1,10,5)
    e = o*3
    ans = st.text_input("Enter energy")
    if st.button("Check Answer"):
        ok = check_answer(e, ans)
        return ok, e
    return None, None

def exp_transpiration():
    show_image("transpiration.png")
    h = st.slider("Humidity",10,90,50)
    r = 100-h
    ans = st.text_input("Enter rate")
    if st.button("Check Answer"):
        ok = check_answer(r, ans)
        return ok, r
    return None, None

def exp_enzyme():
    show_image("enzyme.png")
    t = st.slider("Temperature",0,80,30)
    r = -0.05*(t-37)**2+50
    ans = st.text_input("Enter rate")
    if st.button("Check Answer"):
        ok = check_answer(r, ans)
        return ok, r
    return None, None

# ---------- PHYSICS ----------
def exp_projectile():
    show_image("projectile.png")
    v = st.slider("Velocity",5,50,20)
    a = st.slider("Angle",10,80,45)
    R = (v*v*math.sin(2*math.radians(a)))/9.8
    ans = st.text_input("Enter range")
    if st.button("Check Answer"):
        ok = check_answer(R, ans)
        return ok, R
    return None, None

def exp_hooke():
    show_image("hooke.png")
    k = st.slider("k",10,100,20)
    x = st.slider("Extension",0.1,1.0,0.5)
    F = k*x
    ans = st.text_input("Enter force")
    if st.button("Check Answer"):
        ok = check_answer(F, ans)
        return ok, F
    return None, None

def exp_refraction():
    show_image("refraction.png")
    i = st.slider("Incident angle",10,70,30)
    n = 1.5
    r = math.degrees(math.asin(math.sin(math.radians(i))/n))
    ans = st.text_input("Enter refracted angle")
    if st.button("Check Answer"):
        ok = check_answer(r, ans)
        return ok, r
    return None, None

def exp_magnetic():
    show_image("magnetic.png")
    I = st.slider("Current",1,10,5)
    B = I*2
    ans = st.text_input("Enter field")
    if st.button("Check Answer"):
        ok = check_answer(B, ans)
        return ok, B
    return None, None

def exp_diffusion():
    show_image("diffusion.png")
    t = st.slider("Time",1,60,20)
    d = t*0.2
    ans = st.text_input("Enter distance")
    if st.button("Check Answer"):
        ok = check_answer(d, ans)
        return ok, d
    return None, None

# ---------- CHEMISTRY ----------
def exp_titration():
    show_image("titration.png")
    v = st.slider("Volume",10,50,25)
    s = v*0.1
    ans = st.text_input("Enter strength")
    if st.button("Check Answer"):
        ok = check_answer(s, ans)
        return ok, s
    return None, None

def exp_electrolysis_water():
    show_image("electrolysis_water.png")
    I = st.slider("Current",1,10,3)
    g = I*2
    ans = st.text_input("Enter gas volume")
    if st.button("Check Answer"):
        ok = check_answer(g, ans)
        return ok, g
    return None, None

def exp_electrolysis_cu():
    show_image("electrolysis_cu.png")
    t = st.slider("Time",1,60,20)
    m = t*0.05
    ans = st.text_input("Enter mass")
    if st.button("Check Answer"):
        ok = check_answer(m, ans)
        return ok, m
    return None, None

def exp_reaction_rate():
    show_image("reaction_rate.png")
    t = st.slider("Temperature",20,80,40)
    r = t*1.5
    ans = st.text_input("Enter rate")
    if st.button("Check Answer"):
        ok = check_answer(r, ans)
        return ok, r
    return None, None

def exp_heat_neutralization():
    show_image("heat_neutralization.png")
    v = st.slider("Volume",10,50,20)
    h = v*4.2
    ans = st.text_input("Enter heat")
    if st.button("Check Answer"):
        ok = check_answer(h, ans)
        return ok, h
    return None, None
