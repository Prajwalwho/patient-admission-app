from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401  (importing registers the Patient table)
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # creates tables if missing
    yield


app = FastAPI(title="Patient Admission API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}