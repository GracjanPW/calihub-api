from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreateExercise(BaseModel):
    name: str
    description: Optional[str] = None
    muscle_group: str
    equipment: Optional[list[str]] = None
    difficulty: int


class UpdateExercise(BaseModel):
    description: Optional[str] = None
    equipment: Optional[list[str]] = None
    difficulty: Optional[int] = None
    muscle_group: Optional[str] = None


class Exercise(CreateExercise):
    id: UUID


class ReturnExercises(BaseModel):
    data: list[Exercise]
    total: int
    page: int
    limit: int


class ReturnExercise(BaseModel):
    data: Optional[Exercise] = None
    message: Optional[str] = None


class ReturnExerciseId(BaseModel):
    id: Optional[UUID] = None
    message: Optional[str] = None

