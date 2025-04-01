from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Difficulty(Enum):
    BEGINNER = "beginner"
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ExerciseMuscleGroupReturn(BaseModel):
    id: int
    name: str

class ExerciseEquipmentReturn(BaseModel):
    id: int
    name: str

class CreateExercise(BaseModel):
    name: str
    description: str
    muscle_groups: Optional[list[int]] = None
    equipment: Optional[list[int]] = None
    difficulty: Difficulty


class UpdateExercise(BaseModel):
    description: Optional[str] = None
    equipment: Optional[list[int]] = None
    muscle_groups: Optional[list[int]] = None
    difficulty: Optional[Difficulty] = None


class Exercise(BaseModel):
    id: int
    name: str
    description: str
    muscle_groups: Optional[list[ExerciseMuscleGroupReturn]] = []
    equipment: Optional[list[ExerciseEquipmentReturn]] = []
    difficulty: Difficulty


class ReturnExercises(BaseModel):
    data: list[Exercise]
    total: int
    page: int
    limit: int


class ReturnExercise(BaseModel):
    data: Optional[Exercise] = None
    message: Optional[str] = None


class ReturnExerciseId(BaseModel):
    id: Optional[int] = None
    message: Optional[str] = None
