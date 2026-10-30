from fastapi import FastAPI,Path,HTTPException,Query
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



@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: int = Path(..., description="ID of the patient in the DB")
):
    with open("patients.json", "r") as file:
        data = json.load(file)

    for patient in data:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(staus_code=404,deatil='patient not found ')

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, or BMI"),
    order: str = Query("asc", description="Sort order: asc or desc")
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