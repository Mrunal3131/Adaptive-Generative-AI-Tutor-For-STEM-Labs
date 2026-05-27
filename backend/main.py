from backend.simulation import simulate_ohms_law
from backend.ai_tutor import introduce_experiment, explain_concept
from fastapi import FastAPI
from pydantic import BaseModel
from backend.auth import register_student, login_student

app = FastAPI(title="Virtual STEM Lab Backend")

class RegisterRequest(BaseModel):
    name: str
    roll_no: str
    student_class: int
    password: str

class LoginRequest(BaseModel):
    roll_no: str
    password: str

@app.get("/")
def root():
    return {"message": "Virtual STEM Lab Backend is running"}

@app.post("/register")
def register(request: RegisterRequest):
    return register_student(
        request.name,
        request.roll_no,
        request.student_class,
        request.password
    )

@app.post("/login")
def login(request: LoginRequest):
    return login_student(request.roll_no, request.password)
@app.get("/ai/intro")
def ai_intro(subject: str, experiment: str, class_group: str):
    return {
        "introduction": introduce_experiment(subject, experiment, class_group)
    }


@app.get("/ai/explain")
def ai_explain(subject: str, experiment: str, class_group: str):
    return {
        "explanation": explain_concept(subject, experiment, class_group)
    }
@app.get("/simulate/ohms-law")
def simulate_ohm(voltage: float):
    return simulate_ohms_law(voltage)
