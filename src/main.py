from contextlib import asynccontextmanager
from typing import *

from fastapi import FastAPI
import psycopg_pool

from src.db import lifespan
from .api_routers.exercises.main import router as exercises_router

DATABASE_CONFIG = {
    "user": "app_user",
    "password": "devpassword",
    "host": "localhost",
    "port": 5432,  # Default is 5432
    "database": "calihub_dev_db",
}


app = FastAPI(lifespan=lifespan)


app.include_router(exercises_router, prefix="/api")


@app.get("/")
def read_root():
    return {"hello": "world"}
