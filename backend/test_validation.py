from datetime import timedelta

from pydantic import ValidationError

from app.schemas import PatientCreate, today_ist

VALID = {
    "name": "Ravi Kumar",
    "age": 45,
    "gender": "Male",
    "ward": "ICU",
    "department": "Cardiology",
    "doctor": "Dr. Anil Sharma",
    "admission_date": today_ist(),
}


def expect_ok(label, **overrides):
    PatientCreate(**{**VALID, **overrides})
    print(f"PASS (accepted) : {label}")


def expect_error(label, field, **overrides):
    data = {**VALID, **overrides}
    try:
        PatientCreate(**data)
    except ValidationError as e:
        failed = [err["loc"][0] for err in e.errors()]
        assert field in failed, f"{label}: expected error on {field}, got {failed}"
        msg = [err["msg"] for err in e.errors() if err["loc"][0] == field][0]
        print(f"PASS (rejected) : {label} -> {msg}")
        return
    raise AssertionError(f"{label}: should have been rejected")


# --- valid cases and boundaries ---
expect_ok("valid patient")
expect_ok("age 0 (boundary)", age=0)
expect_ok("age 120 (boundary)", age=120)
expect_ok("admission date today", admission_date=today_ist())
expect_ok("name with space and padding", name="  Anil Kumar  ")

# --- name ---
expect_error("name with digits", "name", name="Ravi123")
expect_error("name with symbol", "name", name="R@vi")
expect_error("empty name", "name", name="")
expect_error("blank name", "name", name="   ")

# --- age ---
expect_error("age -1", "age", age=-1)
expect_error("age 121", "age", age=121)
expect_error("age text", "age", age="abc")
expect_error("age decimal", "age", age=25.5)

# --- selects ---
expect_error("bad gender", "gender", gender="Robot")
expect_error("empty ward", "ward", ward="")
expect_error("bad department", "department", department="Magic")
expect_error("bad doctor", "doctor", doctor="Dr. Nobody")

# --- date ---
expect_error(
    "future date", "admission_date", admission_date=today_ist() + timedelta(days=1)
)

# --- missing required field ---
data = {k: v for k, v in VALID.items() if k != "name"}
try:
    PatientCreate(**data)
    raise AssertionError("missing name should be rejected")
except ValidationError:
    print("PASS (rejected) : missing name field")

print("\nAll validation tests passed.")