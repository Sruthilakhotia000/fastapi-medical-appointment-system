from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI(title="Medical Appointment System")

# =========================
# DATABASE
# =========================
doctors = []
appointments = []
appointment_counter = 1

# =========================
# MODELS
# =========================

class Doctor(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: float = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True


class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False


# =========================
# Q1 HOME
# =========================

@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}


# =========================
# Q2 GET ALL DOCTORS
# =========================

@app.get("/doctors")
def get_doctors():
    return {
        "total": len(doctors),
        "available_count": len([d for d in doctors if d.is_available]),
        "data": doctors
    }


# =========================
# Q4 GET ALL APPOINTMENTS
# =========================

@app.get("/appointments")
def get_appointments():
    return {
        "total": len(appointments),
        "data": appointments
    }


# =========================
# Q5 DOCTORS SUMMARY
# =========================

@app.get("/doctors/summary")
def doctor_summary():
    if not doctors:
        return {"message": "No doctors"}

    specialization_count = {}
    for d in doctors:
        specialization_count[d.specialization] = specialization_count.get(d.specialization, 0) + 1

    return {
        "total_doctors": len(doctors),
        "available": len([d for d in doctors if d.is_available]),
        "most_experienced": max(doctors, key=lambda x: x.experience_years).name,
        "cheapest_fee": min(doctors, key=lambda x: x.fee).fee,
        "specializations": specialization_count
    }

# =========================
# Q7 FILTER DOCTORS
# =========================


@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    max_fee: Optional[float] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None
):
    return filter_doctors_logic(specialization, max_fee, min_experience, is_available)

# =========================
# Q16 SEARCH DOCTORS
# =========================


@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [
        d for d in doctors
        if keyword.lower() in d.name.lower() or keyword.lower() in d.specialization.lower()
    ]
    return {"total_found": len(result), "data": result}

# =========================
# Q17 SORT DOCTORS
# =========================

@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee"):
    return sorted(doctors, key=lambda x: getattr(x, sort_by))


# =========================
# Q18 PAGINATION DOCTORS
# =========================

@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 3):
    total_pages = math.ceil(len(doctors) / limit)
    start = (page - 1) * limit
    end = start + limit
    return {"total_pages": total_pages, "data": doctors[start:end]}


# =========================
# Q20 COMBINED BROWSE
# =========================

@app.get("/doctors/browse")
def browse(
    keyword: str = "",
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):
    result = [
        d for d in doctors
        if keyword.lower() in d.name.lower() or keyword.lower() in d.specialization.lower()
    ]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: getattr(x, sort_by), reverse=reverse)

    total_pages = math.ceil(len(result) / limit)
    start = (page - 1) * limit
    end = start + limit

    return {"total_pages": total_pages, "data": result[start:end]}


# =========================
# Q3 GET DOCTOR BY ID
# =========================

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for d in doctors:
        if d.id == doctor_id:
            return d
    raise HTTPException(status_code=404, detail="Doctor not found")


# =========================
# HELPERS
# =========================

def find_doctor(doctor_id):
    for d in doctors:
        if d.id == doctor_id:
            return d
    return None


def calculate_fee(base_fee, appointment_type):
    appointment_type = appointment_type.lower().strip()

    if appointment_type == "video":
        return int(base_fee * 0.8)
    elif appointment_type == "emergency":
        return int(base_fee * 1.5)
    return (base_fee)


def filter_doctors_logic(specialization, max_fee, min_experience, is_available):
    result = doctors

    if specialization is not None:
        result = [d for d in result if d.specialization.lower() == specialization.lower()]

    if max_fee is not None:
        result = [d for d in result if d.fee <= max_fee]

    if min_experience is not None:
        result = [d for d in result if d.experience_years >= min_experience]

    if is_available is not None:
        result = [d for d in result if d.is_available == is_available]

    return result


# =========================
# Q6 CREATE APPOINTMENT
# =========================

@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appointment_counter

    doctor = find_doctor(req.doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.is_available:
        raise HTTPException(status_code=400, detail="Doctor not available")

    fee = calculate_fee(doctor.fee, req.appointment_type)
    original_fee = doctor.fee

    if req.senior_citizen:
        fee = int(fee * 0.85)

    appointment = {
        "appointment_id": appointment_counter,
        "patient_name": req.patient_name,
        "doctor_name": doctor.name,
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": original_fee,
        "final_fee": int(fee),
        "status": "scheduled"
    }

    doctor.is_available = False

    appointments.append(appointment)
    appointment_counter += 1

    return appointment


# =========================
# Q8 CREATE DOCTOR
# =========================

@app.post("/doctors", status_code=status.HTTP_201_CREATED) 
def create_doctor(doc: Doctor):
    for d in doctors:
        if d.name.lower() == doc.name.lower():
            raise HTTPException(status_code=400, detail="Doctor already exists")
    doctors.append(doc)
    return doc


# =========================
# Q9 UPDATE DOCTOR
# =========================

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, fee: Optional[float] = None, is_available: Optional[bool] = None):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if fee is not None:
        doctor.fee = fee

    if is_available is not None:
        doctor.is_available = is_available

    return doctor


# =========================
# Q10 DELETE DOCTOR
# =========================

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for appt in appointments:
        if appt["doctor_name"] == doctor.name and appt["status"] == "scheduled":
            raise HTTPException(status_code=400, detail="Doctor has active appointments")

    doctors.remove(doctor)
    return {"message": "Doctor deleted successfully"}


# =========================
# Q11 CONFIRM
# =========================

@app.post("/appointments/{id}/confirm")
def confirm(id: int):
    for appt in appointments:
        if appt["appointment_id"] == id:
            appt["status"] = "confirmed"
            return appt
    raise HTTPException(status_code=404, detail="Not found")


# =========================
# Q12 CANCEL
# =========================

@app.post("/appointments/{id}/cancel")
def cancel(id: int):
    for appt in appointments:
        if appt["appointment_id"] == id:
            appt["status"] = "cancelled"
            return appt
    raise HTTPException(status_code=404, detail="Not found")


# =========================
# Q13 COMPLETE
# =========================

@app.post("/appointments/{id}/complete")
def complete(id: int):
    for appt in appointments:
        if appt["appointment_id"] == id:
            appt["status"] = "completed"
            return appt
    raise HTTPException(status_code=404, detail="Not found")


# =========================
# Q14 ACTIVE APPOINTMENTS
# =========================

@app.get("/appointments/active")
def active():
    return [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]


# =========================
# Q15 APPOINTMENTS BY DOCTOR
# =========================

@app.get("/appointments/by-doctor/{doctor_id}")
def by_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return [a for a in appointments if a["doctor_name"] == doctor.name]


# =========================
# Q19 APPOINTMENTS SEARCH/SORT/PAGE
# =========================

@app.get("/appointments/search")
def search_appointments(name: str):
    return [a for a in appointments if name.lower() in a["patient_name"].lower()]


@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "date"):
    return sorted(appointments, key=lambda x: x[sort_by])


@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return appointments[start:end]


