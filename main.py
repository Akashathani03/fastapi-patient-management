from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel
import json

app = FastAPI()


# Pydantic Model
class Patient(BaseModel):
    id: int
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float
    bmi: float
    verdict: str


# -----------------------------
# GET - Get all patients
# -----------------------------
@app.get("/patients")
def get_patients():

    with open("patients.json", "r") as file:
        patients = json.load(file)

    return patients


# -----------------------------
# GET - Home
# -----------------------------
@app.get("/")
def hello():

    return {
        "message": "Patient Management System API"
    }


# -----------------------------
# GET - About
# -----------------------------
@app.get("/about")
def about():

    return {
        "message": "A fully functional API to manage your patient records"
    }


# -----------------------------
# GET - View all patients
# -----------------------------
@app.get("/view")
def view():

    with open("patients.json", "r") as file:
        data = json.load(file)

    return data


# -----------------------------
# GET - View one patient
# -----------------------------
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: int = Path(
        ...,
        description="ID of the patient in the DB"
    )
):

    with open("patients.json", "r") as file:
        data = json.load(file)

    for patient in data:

        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# -----------------------------
# GET - Sort patients
# -----------------------------
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort on the basis of height, weight, or BMI"
    ),
    order: str = Query(
        "asc",
        description="Sort order: asc or desc"
    )
):

    with open("patients.json", "r") as file:
        data = json.load(file)

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort field. Choose height, weight, or bmi"
        )

    if order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="Order must be asc or desc"
        )

    data.sort(
        key=lambda patient: patient[sort_by],
        reverse=(order == "desc")
    )

    return data


# -----------------------------
# POST - Create new patient
# -----------------------------
@app.post("/patient")
def create_patient(patient: Patient):

    with open("patients.json", "r") as file:
        data = json.load(file)

    # Check if ID already exists
    for existing_patient in data:

        if existing_patient["id"] == patient.id:

            raise HTTPException(
                status_code=400,
                detail="Patient with this ID already exists"
            )

    # Add new patient
    data.append(patient.model_dump())

    # Save to JSON file
    with open("patients.json", "w") as file:
        json.dump(data, file, indent=4)

    return {
        "message": "Patient created successfully",
        "patient": patient
    }


# -----------------------------
# PUT - Update patient
# -----------------------------
@app.put("/patient/{patient_id}")
def update_patient(
    patient_id: int,
    updated_patient: Patient
):

    with open("patients.json", "r") as file:
        data = json.load(file)

    for index, patient in enumerate(data):

        if patient["id"] == patient_id:

            # Keep the original ID
            updated_patient.id = patient_id

            # Update patient
            data[index] = updated_patient.model_dump()

            # Save changes
            with open("patients.json", "w") as file:
                json.dump(data, file, indent=4)

            return {
                "message": "Patient updated successfully",
                "patient": updated_patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# -----------------------------
# DELETE - Delete patient
# -----------------------------
@app.delete("/patient/{patient_id}")
def delete_patient(patient_id: int):

    with open("patients.json", "r") as file:
        data = json.load(file)

    for index, patient in enumerate(data):

        if patient["id"] == patient_id:

            # Remove patient
            deleted_patient = data.pop(index)

            # Save changes
            with open("patients.json", "w") as file:
                json.dump(data, file, indent=4)

            return {
                "message": "Patient deleted successfully",
                "patient": deleted_patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )