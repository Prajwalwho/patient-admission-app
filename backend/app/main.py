import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import models  # noqa: F401  (importing registers the Patient table)
from .database import Base, engine
from .routers import patients

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # creates tables if missing
    yield


app = FastAPI(title="Patient Admission API", lifespan=lifespan)

# --- CORS: allow the React app to call this API ---
origins = {"http://localhost:5173", "http://127.0.0.1:5173"}
for url in os.getenv("FRONTEND_URL", "").split(","):
    if url.strip():
        origins.add(url.strip().rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(origins),
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Clear, consistent error messages ---
def clean_message(err: dict) -> str:
    field = str(err["loc"][-1]) if err["loc"] else "body"
    label = field.replace("_", " ").capitalize()
    err_type = err["type"]

    if err_type in ("missing", "string_type"):
        return f"{label} is required"
    if err_type.startswith("int_"):
        if field == "age":
            return "Age must be a whole number between 0 and 120"
        return f"{label} must be a whole number"
    if err_type.startswith("date_"):
        return f"{label} must be a valid date (YYYY-MM-DD)"
    return err["msg"].removeprefix("Value error, ")


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for err in exc.errors():
        field = str(err["loc"][-1]) if err["loc"] else "body"
        errors.setdefault(field, clean_message(err))  # first error per field
    return JSONResponse(
        status_code=422,
        content={"message": "Validation failed", "errors": errors},
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


app.include_router(patients.router)


@app.get("/health")
def health():
    return {"status": "ok"}