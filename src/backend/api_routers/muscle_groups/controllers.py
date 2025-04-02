from typing import Optional
import psycopg
import psycopg.rows

from src.backend.api_routers.muscle_groups.modals import CreateMuscleGroup, UpdateMuscleGroup

# ------------------------------------------------------------------------------------------------------------------------------------

async def get_muscle_groups(
        conn:  any, 
        name:  Optional[str] = None, 
        page:  int           = 1, 
        limit: int           = 10
):
    
    query   = "SELECT id, name FROM muscle_groups WHERE 1=1"
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
            "SELECT COUNT(*) as count FROM muscle_groups WHERE 1=1"+limit_filter, 
            (
                *limit_params,
            )
        )
        
        count_res = await cursor.fetchone()
        total = count_res['count']

    return res, total

# ------------------------------------------------------------------------------------------------------------------------------------

async def get_muscle_group(
    conn: any,
    id:   int
):
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            "SELECT id, name FROM muscle_groups WHERE id = %s", 
            (
                id, 
            )
        )

        res = await cursor.fetchone()
    
    return res

# ------------------------------------------------------------------------------------------------------------------------------------

async def create_muscle_group(
    conn: any,
    data: CreateMuscleGroup
): 
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            "INSERT INTO muscle_groups (name) VALUES (%s) RETURNING id",
            (
                *data,
            )
        )

        res = await cursor.fetchone()

    return res['id']

# ------------------------------------------------------------------------------------------------------------------------------------

async def update_muscle_group(
    conn: any,
    id:   int,
    data: UpdateMuscleGroup
):
    async with conn.transaction():
        async with conn.cursor(
            row_factory=psycopg.rows.dict_row
        ) as cursor:
            await cursor.execute(
                "UPDATE muscle_groups SET name = COALESCE(%s, name) WHERE id = %s RETURNING id",
                (
                    *data,
                    id
                )
            )

            res = await cursor.fetchone()

    return res['id']

# ------------------------------------------------------------------------------------------------------------------------------------

async def delete_muscle_group(
    conn: any,
    id:   int
):
    async with conn.cursor(
        row_factory = psycopg.rows.dict_row
    ) as cursor:
        await cursor.execute(
            "DELETE FROM muscle_groups WHERE id = %s RETURNING id",
            (
                id,
            )
        )

        res = await cursor.fetchone()

    return res['id']

# ------------------------------------------------------------------------------------------------------------------------------------
