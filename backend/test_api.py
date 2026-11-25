from datetime import timedelta

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import today_ist

VALID = {
    "name": "Zyxwv Testpatient",
    "age": 45,
    "gender": "Male",
    "ward": "ICU",
    "department": "Cardiology",
    "doctor": "Dr. Anil Sharma",
    "admission_date": str(today_ist()),
}


def check(label, condition):
    assert condition, f"FAILED: {label}"
    print(f"PASS: {label}")


with TestClient(app) as client:
    created_id = None
    try:
        # options
        r = client.get("/options")
        check("GET /options returns dropdown lists", r.status_code == 200 and "wards" in r.json())

        # create
        r = client.post("/patients", json=VALID)
        check("POST /patients -> 201", r.status_code == 201)
        created_id = r.json()["id"]
        check("new patient status is Admitted", r.json()["status"] == "Admitted")

        # list + filters + search
        r = client.get("/patients")
        check("list includes new patient", created_id in [p["id"] for p in r.json()])

        r = client.get("/patients", params={"ward": "ICU", "doctor": "Dr. Anil Sharma"})
        ids = [p["id"] for p in r.json()]
        check("filter by ward + doctor finds patient", created_id in ids)
        check("filter results all match ward", all(p["ward"] == "ICU" for p in r.json()))

        r = client.get("/patients", params={"ward": "Maternity Ward", "search": "Zyxwv"})
        check("wrong ward filter excludes patient", created_id not in [p["id"] for p in r.json()])

        r = client.get("/patients", params={"search": "zyxwv"})
        check("search by name is case-insensitive", created_id in [p["id"] for p in r.json()])

        r = client.get("/patients", params={"search": "%"})
        check("search with % does not match everything", created_id not in [p["id"] for p in r.json()])

        # validation through the API
        r = client.post("/patients", json={**VALID, "name": "Ravi123"})
        check("name with digits -> 422", r.status_code == 422 and "name" in r.json()["errors"])

        r = client.post("/patients", json={**VALID, "age": 121})
        check("age 121 -> 422 with message", r.status_code == 422 and "0 and 120" in r.json()["errors"]["age"])

        r = client.post("/patients", json={**VALID, "age": "abc"})
        check("age text -> 422", r.status_code == 422 and "age" in r.json()["errors"])

        r = client.post("/patients", json={**VALID, "ward": "Moon Base"})
        check("invalid ward -> 422", r.status_code == 422 and "ward" in r.json()["errors"])

        future = str(today_ist() + timedelta(days=1))
        r = client.post("/patients", json={**VALID, "admission_date": future})
        check("future date -> 422", r.status_code == 422 and "future" in r.json()["errors"]["admission_date"])

        body = {k: v for k, v in VALID.items() if k != "doctor"}
        r = client.post("/patients", json=body)
        check("missing doctor -> 422", r.status_code == 422 and r.json()["errors"]["doctor"] == "Doctor is required")

        # edit
        r = client.put(f"/patients/{created_id}", json={**VALID, "age": 50, "ward": "General Ward"})
        check("PUT updates fields", r.status_code == 200 and r.json()["age"] == 50 and r.json()["ward"] == "General Ward")

        r = client.put(f"/patients/{created_id}", json={**VALID, "age": -5})
        check("PUT validates too -> 422", r.status_code == 422)

        # discharge
        r = client.patch(f"/patients/{created_id}/discharge")
        check("discharge -> status Discharged", r.status_code == 200 and r.json()["status"] == "Discharged")

        r = client.patch(f"/patients/{created_id}/discharge")
        check("discharging twice -> 400", r.status_code == 400)

        # 404
        r = client.get("/patients/999999")
        check("unknown id -> 404 with message", r.status_code == 404 and "message" in r.json())

    finally:
        if created_id is not None:
            r = client.delete(f"/patients/{created_id}")
            print("cleanup delete status:", r.status_code)
            r = client.get(f"/patients/{created_id}")
            check("deleted patient is gone (404)", r.status_code == 404)

print("\nAll API tests passed.")