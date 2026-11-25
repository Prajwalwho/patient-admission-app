from datetime import date

from app import models
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
db = SessionLocal()

p = models.Patient(
    name="Test Patient",
    age=30,
    gender="Male",
    ward="ICU",
    department="Cardiology",
    doctor="Dr. Anil Sharma",
    admission_date=date(2026, 11, 20),
)
db.add(p)
db.commit()
db.refresh(p)
print("Inserted id:", p.id, "| default status:", p.status)

found = db.get(models.Patient, p.id)
assert found is not None and found.name == "Test Patient"

db.delete(found)
db.commit()
db.close()
print("Row read back and cleaned up. Model works.")