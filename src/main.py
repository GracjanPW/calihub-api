from typing import *

from fastapi import FastAPI
from .api_routers import exercises

app = FastAPI()

app.include_router(exercises.router, prefix="/api")

@app.get("/")
def read_root():
    return {"hello":"world"}

