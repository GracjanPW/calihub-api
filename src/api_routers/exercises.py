from typing import Optional
from fastapi import APIRouter, Response, status
from pydantic import BaseModel

# region: modals
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
    id: int

class ReturnExercises(BaseModel):
    data: list[Exercise]

class ReturnExercise(BaseModel):
    data: Optional[Exercise] = None
    message: Optional[str] = None

class ReturnExerciseId(BaseModel):
    id: Optional[int] = None
    message: Optional[str] = None


# endregion: modals

router = APIRouter()

@router.get("/exercises/", status_code=status.HTTP_200_OK)
def get_exercises() -> ReturnExercises:
    return ReturnExercises(data=[Exercise(id=1, name="Bench Press", muscle_group="Chest", difficulty=3)])

@router.get("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
def get_exercise(exercise_id: int) -> ReturnExercise:
    if exercise_id == 1:
        return ReturnExercise(data=Exercise(id=1, name="Bench Press", muscle_group="Chest", difficulty=3))
    return ReturnExercise(message="Exercise not found")

@router.post("/exercises/", status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: CreateExercise) -> ReturnExerciseId:
    print(exercise)
    return ReturnExerciseId(id=2)

@router.put("/exercises/{exercise_id}")
def update_exercise(exercise_id: int, exercise: UpdateExercise) -> ReturnExerciseId:
    return ReturnExerciseId(id=exercise_id)

@router.delete("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
def delete_exercise(exercise_id: int, response: Response) -> ReturnExerciseId:
    if exercise_id == 1:
        return ReturnExerciseId(id=exercise_id)
    response.status_code = 404
    return ReturnExerciseId(message="Exercise not found")