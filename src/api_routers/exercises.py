from fastapi import APIRouter, Response, status
from pydantic import BaseModel

# region: modals
class CreateExercise(BaseModel):
    name: str
    description: str | None = None
    muscle_group: str
    equipment: str | None = None
    difficulty: int

class UpdateExercise():
    description: str | None = None
    equipment: str | None = None
    difficulty: int | None = None
    muscle_group: str | None = None

class Exercise(CreateExercise):
    id: int

class ReturnExercises(BaseModel):
    data: list[Exercise]

class ReturnExercise(BaseModel):
    data: Exercise | None
    message: str | None = None

class ReturnExerciseId(BaseModel):
    id: int | None
    message: str | None = None


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