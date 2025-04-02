from pathlib import Path
from fastapi.staticfiles import StaticFiles
from .backend.api_routers.auth.main import router as auth_router
from .backend.api_routers.exercises.main import router as exercises_router
from .backend.api_routers.muscle_groups.main import router as muscle_group_router
from src.backend.db import lifespan
from fastapi import FastAPI
from typing import *
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(docs_url="/fastapi_docs",lifespan=lifespan)


app.include_router(exercises_router, prefix="/api")
app.include_router(muscle_group_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")


STATIC_PATH = Path(__file__).parent.resolve() / "frontend" / "dist"
app.mount("/", StaticFiles(directory=STATIC_PATH, html=True), name="frontend")


@app.get("/")
def read_root():
    return {"hello": "world"}
