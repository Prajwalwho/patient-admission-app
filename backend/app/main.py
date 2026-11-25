from fastapi import FastAPI

app = FastAPI(title="Patient Admission API")

@app.get("/health")
def health():
    return {"status": "ok"}