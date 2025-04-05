

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, Query

from src.backend.api_routers.equipment import controllers as EquipmentController 
from src.backend.api_routers.equipment.modals import CreateEquipment, ReturnEquipmentId, ReturnEquipmentAll, ReturnEquipment, UpdateEquipment
from src.backend.auth_lib.main import get_current_user, is_admin
from src.backend.db import get_db
from src.backend.redis import rate_limit_dependency


router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------------------------

@router.get("/equipment", status_code=status.HTTP_200_OK)
async def get_equipment(
    response:   Response,
    user =      Depends(get_current_user),
    name:       Optional[str]   = Query(alias="search", default=None, description="Search equipment by name"),
    limit:      int             = Query(default=10, le=100, description="Number of items per page (max 100)"),
    page:       int             = Query(default=1, ge=1, description="Page number"),
    conn                        = Depends(get_db)
) -> ReturnEquipmentAll:
    rate_limit_dependency(user_id=user['sub'], user_quota=user['quota'])
    
    try:
        res, total = await EquipmentController.get_equipment(
            conn = conn, 
            name = name, 
            page = page, 
            limit = limit
        )

        return ReturnEquipmentAll(
            data  = res,
            total = total,
            limit = limit,
            page  = page
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500, 
            detail      = "Trouble getting equipment, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.get("/equipment/{equipment_id}")
async def get_equipment_by_id(
    response:       Response,
    equipment_id:   int,
    user =          Depends(get_current_user),
    conn =          Depends(get_db)
) -> ReturnEquipment:
    rate_limit_dependency(user_id=user['sub'], user_quota=user['quota'])

    try:
        res = await EquipmentController.get_equipment_by_id(
            conn = conn,
            id   = equipment_id
        )

        return ReturnEquipment(
            data = res
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble getting equipment, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.post("/equipment", status_code=status.HTTP_201_CREATED)
async def create_equipment(
    response:        Response,
    new_equipment:   CreateEquipment,
    conn =           Depends(get_db),
    _admin_user =    Depends(is_admin)
):  
    try:
        res = await EquipmentController.create_equipment(
            conn = conn,
            data = new_equipment
        )

        return ReturnEquipmentId(
            id      = res,
            message = "Successfully created equipment"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble creating equipment, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.put("/equipment/{equipment_id}")
async def update_equipment(
    response:          Response,
    equipment_id:      int,
    equipment_update:  UpdateEquipment,
    conn =             Depends(get_db),
    _admin_user =      Depends(is_admin)
):
    try:
        res = await EquipmentController.update_equipment(
            conn = conn,
            id   = equipment_id,
            data = equipment_update
        )

        return ReturnEquipmentId(
            id      = res,
            message = "Successfully updated equipment"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble updating equipment, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

@router.delete("/equipment/{equipment_id}")
async def delete_equipment(
    response:       Response,
    equipment_id:   int,
    conn =          Depends(get_db),
    _admin_user =   Depends(is_admin)
):
    try:
        res = await EquipmentController.delete_equipment(
            conn = conn,
            id   = equipment_id
        )

        return ReturnEquipmentId(
            id      = res,
            message = "Successfully deleted equipment"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = 500,
            detail      = "Trouble deleting equipment, try again later"
        )

# ------------------------------------------------------------------------------------------------------------------------------------

