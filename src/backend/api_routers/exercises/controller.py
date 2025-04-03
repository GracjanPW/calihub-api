from typing import Optional
from fastapi import HTTPException
import psycopg
from psycopg.errors import ForeignKeyViolation

# TODO: implement filtering by multiple muscle groups and equipment


async def get_exercises(
    conn,
    name: Optional[str] = None,
    muscle_group: Optional[str] = None,
    equipment: Optional[str] = None,
    difficulty: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    query = """
    SELECT 
        e.id,
        e.name,
        e.description,
        e.difficulty,
        COALESCE(
            array_agg(
                DISTINCT jsonb_build_object(
                    'id', mg.id,
                    'name', mg.name
                )
            ) FILTER (WHERE mg.id IS NOT NULL AND mg.name IS NOT NULL),
            '{}'
        ) AS muscle_groups,
        COALESCE(
            array_agg(
                DISTINCT jsonb_build_object(
                    'id', q.id,
                    'name', q.name
                )
            ) FILTER (WHERE q.id IS NOT NULL AND q.name IS NOT NULL),
            '{}'
        ) AS equipment
    FROM exercises e
    LEFT JOIN exercise_muscle_groups emg ON e.id = emg.exercise_id
    LEFT JOIN muscle_groups mg ON mg.id = emg.muscle_group_id
    LEFT JOIN exercise_equipment eq ON e.id = eq.exercise_id
    LEFT JOIN equipment q ON q.id = eq.equipment_id
    WHERE 1 = 1"""

    count_query = """
    SELECT COUNT(DISTINCT e.id) as total
    FROM exercises e
    LEFT JOIN exercise_muscle_groups emg ON e.id = emg.exercise_id
    LEFT JOIN muscle_groups mg ON mg.id = emg.muscle_group_id
    LEFT JOIN exercise_equipment eq ON e.id = eq.exercise_id
    LEFT JOIN equipment q ON q.id = eq.equipment_id
    WHERE 1 = 1"""

    filters = ""
    params = []
    
    if name:
        filters += " AND e.name ILIKE %s"
        params.append(f"%{name}%")
    if muscle_group:
        filters += " AND mg.name ILIKE %s"
        params.append(f"%{muscle_group}%")
    if equipment:
        filters += " AND q.name ILIKE %s"
        params.append(f"%{equipment}%")
    if difficulty:
        filters += " AND e.difficulty = %s"
        params.append(difficulty)
        
    group_by = " GROUP BY e.id, e.name, e.description, e.difficulty"
    limit_filter = " ORDER BY e.name LIMIT %s OFFSET %s"
    params.extend([limit, (page - 1) * limit])

    total = 0
    async with conn.transaction():
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute(query+filters+group_by+limit_filter, (*params,))
            exercises = await cursor.fetchall()
            
            await cursor.execute(count_query+filters, (*params[:-2],))
            count_result = await cursor.fetchone()
            total = count_result['total'] if count_result else 0

    return exercises, total


async def get_exercise(conn, exercise_id: int):
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        await cursor.execute("""SELECT e.id, e.name, e.description, e.difficulty, 
                COALESCE(array_agg(
                    DISTINCT jsonb_build_object('id',mg.id,'name',mg.name)) FILTER (WHERE mg.id IS NOT NULL AND mg.name IS NOT NULL),
                    '{}'
                ) as muscle_groups,
                COALESCE(array_agg(
                    DISTINCT jsonb_build_object('id',q.id,'name',q.name)) FILTER (WHERE q.id IS NOT NULL AND q.name IS NOT NULL),
                    '{}'
                ) as equipment
                FROM exercises e 
                LEFT JOIN exercise_muscle_groups emg ON e.id = emg.exercise_id
                LEFT JOIN muscle_groups mg ON mg.id = emg.muscle_group_id
                LEFT JOIN exercise_equipment eq ON e.id = eq.exercise_id
                LEFT JOIN equipment q ON eq.equipment_id = q.id
                WHERE e.id = %s 
                GROUP BY e.id""",
                             (exercise_id,))
        res = await cursor.fetchone()
    return res


async def create_exercise(conn, exercise):
    try:
        async with conn.transaction():
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
                await cursor.execute("INSERT INTO exercises (name, description, difficulty) VALUES (%s, %s, %s) RETURNING id", (exercise.name, exercise.description, exercise.difficulty.value))
                res = await cursor.fetchone()
                id = res['id']

                for i in exercise.equipment:
                    await cursor.execute("INSERT INTO exercise_equipment (exercise_id, equipment_id) VALUES (%s,%s)", (id, i))

                for i in exercise.muscle_groups:
                    await cursor.execute("INSERT INTO exercise_muscle_groups (exercise_id, muscle_group_id) VALUES (%s,%s)", (id, i))

        return id
    except ForeignKeyViolation as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid data, muscle_group or equipment doesn't exist"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


async def update_exercise(conn, exercise_id:int, exercise):
    try:
        async with conn.transaction():
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
                await cursor.execute(
                    """UPDATE exercises SET 
                            description = COALESCE(%s, description), 
                            difficulty = COALESCE(%s, difficulty)
                        WHERE id = %s RETURNING id
                    """, (exercise.description, exercise.difficulty.value, exercise_id))
                res = await cursor.fetchone()
                id = res['id']
                print(id)

                if exercise.equipment is not None:
                    await cursor.execute(
                        "DELETE FROM exercise_equipment WHERE exercise_id = %s",
                        (exercise_id,)
                    )
                    for i in exercise.equipment:
                        await cursor.execute(
                            "INSERT INTO exercise_equipment (exercise_id, equipment_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            (id, i))
                print('he')
                if exercise.muscle_groups is not None:
                    await cursor.execute(
                        "DELETE FROM exercise_muscle_groups WHERE exercise_id = %s",
                        (exercise_id,)
                    )
                    for i in exercise.muscle_groups:
                        await cursor.execute(
                            "INSERT INTO exercise_muscle_groups (exercise_id, muscle_group_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            (id, i))

        return id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Unhandled error")


async def delete_exercise(conn, exercise_id):
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM exercises WHERE id = %s", (exercise_id,))
    if cursor.rowcount:
        return cursor.rowcount
    return None
