from .api_routers.auth.main import router as auth_router
from .api_routers.exercises.main import router as exercises_router
from src.db import lifespan
from fastapi import FastAPI
from typing import *
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(lifespan=lifespan)


app.include_router(exercises_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")


@app.get("/")
def read_root():
    return {"hello": "world"}
