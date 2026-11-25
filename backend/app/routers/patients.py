from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from .. import constants, models, schemas
from ..database import get_db

router = APIRouter()


def get_patient_or_404(db: Session, patient_id: int) -> models.Patient:
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(
            status_code=404, detail=f"Patient with id {patient_id} not found"
        )
    return patient


@router.get("/options")
def get_options():
    """Single source of truth for the frontend dropdowns."""
    return {
        "genders": constants.GENDERS,
        "wards": constants.WARDS,
        "departments": constants.DEPARTMENTS,
        "doctors": constants.DOCTORS,
    }


@router.post("/patients", response_model=schemas.PatientResponse, status_code=201)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = models.Patient(
        **payload.model_dump(), status=constants.STATUS_ADMITTED
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/patients", response_model=list[schemas.PatientResponse])
def list_patients(
    ward: Optional[str] = None,
    department: Optional[str] = None,
    doctor: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Patient)

    if ward:
        query = query.filter(models.Patient.ward == ward)
    if department:
        query = query.filter(models.Patient.department == department)
    if doctor:
        query = query.filter(models.Patient.doctor == doctor)
    if search and search.strip():
        term = search.strip()
        # escape LIKE wildcards so "%" or "_" are treated as plain characters
        term = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        query = query.filter(models.Patient.name.ilike(f"%{term}%", escape="\\"))

    return query.order_by(models.Patient.id.desc()).all()


@router.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return get_patient_or_404(db, patient_id)


@router.put("/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int, payload: schemas.PatientUpdate, db: Session = Depends(get_db)
):
    patient = get_patient_or_404(db, patient_id)
    for field, value in payload.model_dump().items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/patients/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_or_404(db, patient_id)
    db.delete(patient)
    db.commit()
    return Response(status_code=204)


@router.patch(
    "/patients/{patient_id}/discharge", response_model=schemas.PatientResponse
)
def discharge_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_or_404(db, patient_id)
    if patient.status == constants.STATUS_DISCHARGED:
        raise HTTPException(status_code=400, detail="Patient is already discharged")
    patient.status = constants.STATUS_DISCHARGED
    db.commit()
    db.refresh(patient)
    return patient