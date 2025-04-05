

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, Query

from src.backend.api_routers.muscle_groups import controllers as MuscleGroupController 
from src.backend.api_routers.muscle_groups.modals import CreateMuscleGroup, ReturnMuscleGroupId, ReturnMuscleGroups, ReturnMuscleGroup, UpdateMuscleGroup
from src.backend.auth_lib.main import get_current_user, is_admin
from src.backend.db import get_db
from src.backend.redis import rate_limit_dependency


router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------------------------

@router.get("/muscle_groups", status_code=status.HTTP_200_OK)
async def get_muscle_groups(
    response:   Response,
    user                        = Depends(get_current_user),
    name:       Optional[str]   = Query(alias="search", default=None, description="Search muscle groups by name"),
    limit:      int             = Query(default=10, le=100, description="Number of items per page (max 100)"),
    page:       int             = Query(default=1, ge=1, description="Page number"),
    conn                        = Depends(get_db)
) -> ReturnMuscleGroups:
    rate_limit_dependency(user_id=user['sub'], user_quota=user['quota'])
    try:
        res, total = await MuscleGroupController.get_muscle_groups(
            conn = conn, 
            name = name, 
            page = page, 
            limit = limit
        )

        return ReturnMuscleGroups(
            data  = res,
            total = total,
            limit = limit,
            page  = page
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500, 
            detail      = "Trouble getting exercises, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.get("/muscle_groups/{muscle_group_id}")
async def get_muscle_group(
    response:           Response,
    muscle_group_id:    int,
    user =              Depends(get_current_user),
    conn =              Depends(get_db)
) -> ReturnMuscleGroup:
    rate_limit_dependency(user_id=user['sub'], user_quota=user['quota'])
    
    try:
        res = await MuscleGroupController.get_muscle_group(
            conn = conn,
            id   = muscle_group_id
        )

        return ReturnMuscleGroup(
            data = res
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.post("/muscle_groups", status_code=status.HTTP_201_CREATED)
async def create_muscle_group(
    response:           Response,
    new_muscle_group:   CreateMuscleGroup,
    conn =              Depends(get_db),
    _admin_user =       Depends(is_admin)
):
    try:
        res = await MuscleGroupController.create_muscle_group(
            conn = conn,
            data = new_muscle_group
        )

        return ReturnMuscleGroupId(
            id      = res,
            message = "Successfully created muscle group"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble creating muscle group"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.put("/muscle_groups/{muscle_group_id}")
async def update_muscle_group(
    response:            Response,
    muscle_group_id:     int,
    muscle_group_update: UpdateMuscleGroup,
    conn =               Depends(get_db),
    _admin_user =        Depends(is_admin)
):
    try:
        res = await MuscleGroupController.update_muscle_group(
            conn = conn,
            id   = muscle_group_id,
            data = muscle_group_update
        )

        return ReturnMuscleGroupId(
            id      = res,
            message = "Successfully updated muscle group"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble updating muscle group"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.delete("/muscle_groups/{muscle_group_id}")
async def delete_muscle_group(
    response:           Response,
    muscle_group_id:    int,
    conn =              Depends(get_db),
    _admin_user =       Depends(is_admin)
):
    try:
        res = await MuscleGroupController.delete_muscle_group(
            conn = conn,
            id   = muscle_group_id
        )

        return ReturnMuscleGroupId(
            id      = res,
            message = "Successfully deleted muscle group"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble deleting muscle group"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

