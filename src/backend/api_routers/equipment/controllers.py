from typing import Optional
import psycopg
import psycopg.rows

from src.backend.api_routers.equipment.modals import CreateEquipment, UpdateEquipment

# ------------------------------------------------------------------------------------------------------------------------------------

async def get_equipment(
        conn:  any, 
        name:  Optional[str] = None, 
        page:  int           = 1, 
        limit: int           = 10
):
    
    query   = "SELECT id, name, description FROM equipment WHERE 1=1"
    filters = ""
    params  = []

    if name:
        filters += " AND name ILIKE %s"
        params.append(f"%{name}%")

    limit_filter = " LIMIT %s OFFSET %s"
    limit_params = [limit, (page-1)*limit]
    
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            query+filters+limit_filter, 
            (
                *params,
                *limit_params,
            )
        )

        res = await cursor.fetchall()

        await cursor.execute(
            "SELECT COUNT(*) as count FROM equipment WHERE 1=1"+limit_filter, 
            (
                *limit_params,
            )
        )
        
        count_res = await cursor.fetchone()
        total = count_res['count']

    return res, total

# ------------------------------------------------------------------------------------------------------------------------------------

async def get_equipment_by_id(
    conn: any,
    id:   int
):
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            "SELECT id, name, description FROM equipment WHERE id = %s", 
            (
                id, 
            )
        )

        res = await cursor.fetchone()
    
    return res

# ------------------------------------------------------------------------------------------------------------------------------------

async def create_equipment(
    conn: any,
    data: CreateEquipment
): 
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            "INSERT INTO equipment (name, description) VALUES (%s, %s) RETURNING id",
            (
                *data,
            )
        )

        res = await cursor.fetchone()

    return res['id']

# ------------------------------------------------------------------------------------------------------------------------------------

async def update_equipment(
    conn: any,
    id:   int,
    data: UpdateEquipment
):
    async with conn.transaction():
        async with conn.cursor(
            row_factory=psycopg.rows.dict_row
        ) as cursor:
            await cursor.execute(
                "UPDATE equipment SET name = COALESCE(%s, name), description = COALESCE(%s, description) WHERE id = %s RETURNING id",
                (
                    *data,
                    id
                )
            )

            res = await cursor.fetchone()

    return res['id']

# ------------------------------------------------------------------------------------------------------------------------------------

async def delete_equipment(
    conn: any,
    id:   int
):
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            "DELETE FROM equipment WHERE id = %s RETURNING id",
            (
                id,
            )
        )

        res = await cursor.fetchone()

    return res['id']

# ------------------------------------------------------------------------------------------------------------------------------------
