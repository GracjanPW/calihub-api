from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from src.backend.api_routers.exercises import controller as ExerciseController
from psycopg.errors import ForeignKeyViolation
from src.backend.api_routers.exercises.modals import CreateExercise, ReturnExercise, ReturnExerciseId, ReturnExercises, UpdateExercise
from src.backend.auth_lib.main import is_admin
from src.backend.db import get_db

router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------------------------

@router.get("/exercises", status_code=status.HTTP_200_OK)
async def get_exercises(
    name:           Optional[str] = Query(None, alias="search", description="Search exercises by name"),
    muscle_group:   Optional[str] = Query(None, description="Filter by category"),
    equipment:      Optional[str] = Query(None, description="Filter by category"),
    difficulty:     Optional[str] = Query(None, description="Filter by difficulty level"),
    page:           int           = Query(1, ge=1, description="Page number (1-based index)"),
    limit:          int           = Query(10, le=100, description="Number of items per page (max 100)"),
    conn                          = Depends(get_db)
) -> ReturnExercises:
    try:
        # Get exercises from controller with search, filters, and pagination
        res, total = await ExerciseController.get_exercises(
            conn         = conn, 
            name         = name, 
            muscle_group = muscle_group, 
            equipment    = equipment, 
            difficulty   = difficulty, 
            page         = page, 
            limit        = limit
        )

        # Return exercises data, total count, current page, and limit
        return ReturnExercises(
            data  = res, 
            total = total, 
            page  = page, 
            limit = limit
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble getting exercises, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.get("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
async def get_exercise(
    exercise_id:  int, 
    response:     Response, 
    conn =        Depends(get_db)
) -> ReturnExercise:
    try:
        # Find and return exercise with given id
        res = await ExerciseController.get_exercise(
            conn        = conn, 
            exercise_id = exercise_id
        )
        if res:
            return ReturnExercise(
                data = res
            )
        
        response.status_code = 404

        return ReturnExercise(
            message = "Exercise not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble getting exercise, try again later"
        )
    

# ------------------------------------------------------------------------------------------------------------------------------------

@router.post("/exercises", status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise:     CreateExercise,
    response:     Response, 
    conn =        Depends(get_db),
    _admin_user = Depends(is_admin) 
) -> ReturnExerciseId:
    try:
        # Create exercise
        res = await ExerciseController.create_exercise(
            conn     = conn, 
            exercise = exercise
        )
    
        if res:
            return ReturnExerciseId(
                id  = res
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble creating exercise, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.put("/exercises/{exercise_id}")
async def update_exercise(
    exercise_id:        int, 
    exercise_changes:   UpdateExercise, 
    response:           Response, 
    conn =              Depends(get_db),
    _admin_user =          Depends(is_admin)  
) -> ReturnExerciseId:
    try:
        res = await ExerciseController.update_exercise(
            conn        = conn, 
            exercise_id = exercise_id, 
            exercise    = exercise_changes
        )

        if res:
            return ReturnExerciseId(
                id = res
            )
    
        response.status_code = 404
    
        return ReturnExerciseId(
            message = "Exercise not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble updating exercise, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.delete("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
async def delete_exercise(
    exercise_id:    int, 
    response:       Response, 
    conn=           Depends(get_db),
    _admin_user =   Depends(is_admin) 
) -> ReturnExerciseId:
    try:
        rowcount = await ExerciseController.delete_exercise(
            conn        = conn, 
            exercise_id = exercise_id
        )
        if rowcount:
            return ReturnExerciseId(
                id = exercise_id
            )
    
        response.status_code = 404
    
        return ReturnExerciseId(
            message = "Exercise not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble deleting exercise, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------
