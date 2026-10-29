from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/patients")
def get_patients():
    with open("patients.json", "r") as file:
        patients = json.load(file)

    return patients

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    with open("patients.json", "r") as file:
        data = json.load(file)

    return data