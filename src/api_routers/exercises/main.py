from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
import psycopg
from src.api_routers.exercises import controller as ExerciseController

from src.api_routers.exercises.modals import CreateExercise, ReturnExercise, ReturnExerciseId, ReturnExercises, UpdateExercise
from src.db import get_db

router = APIRouter()


@router.get("/exercises", status_code=status.HTTP_200_OK)
async def get_exercises(
    name: Optional[str] = Query(None, alias="search", description="Search exercises by name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    page: int = Query(1, ge=1, description="Page number (1-based index)"),
    limit: int = Query(10, le=100, description="Number of items per page (max 100)"),
    conn=Depends(get_db)
) -> ReturnExercises:
    # Get exercises from controller with search, filters, and pagination
    res, total = await ExerciseController.get_exercises(
        conn, name=name, category=category, difficulty=difficulty, page=page, limit=limit
    )

    # Return exercises data, total count, current page, and limit
    return ReturnExercises(data=res, total=total, page=page, limit=limit)

@router.get("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
async def get_exercise(exercise_id: UUID, response: Response, conn=Depends(get_db)) -> ReturnExercise:
    res = await ExerciseController.get_exercise(conn, exercise_id)
    if res:
        return ReturnExercise(data=res)
    response.status_code = 404
    return ReturnExercise(message="Exercise not found")


@router.post("/exercises/", status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise: CreateExercise, conn=Depends(get_db)) -> ReturnExerciseId:
    res = await ExerciseController.create_exercise(conn, exercise)
    if res:
        return ReturnExerciseId(id=res[0])
    return ReturnExerciseId(message="Failed to create exercise")


@router.put("/exercises/{exercise_id}")
async def update_exercise(exercise_id: UUID, exercise: UpdateExercise, response: Response, conn = Depends(get_db)) -> ReturnExerciseId:
    res = await ExerciseController.update_exercise(conn, exercise_id, exercise)
    if res:
        return ReturnExerciseId(id=res[0])
    response.status_code = 404
    return ReturnExerciseId(message="Exercise not found")

@router.delete("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
async def delete_exercise(exercise_id: UUID, response: Response, conn = Depends(get_db)) -> ReturnExerciseId:
    rowcount = await ExerciseController.delete_exercise(conn, exercise_id)
    if rowcount:
        return ReturnExerciseId(id=exercise_id)
    response.status_code = 404
    return ReturnExerciseId(message="Exercise not found")
