from typing import Optional
import psycopg


async def get_exercises(
    conn, 
    name:Optional[str] = None, 
    category: Optional[str] = None,     
    difficulty: Optional[str] = None, 
    page: int = 1, 
    limit: int = 10
):
    query = "SELECT * FROM exercises WHERE 1 = 1"
    filters = ""
    params = []
    if name:
        filters += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if category:
        filters += " AND muscle_group = %s"
        params.append(category)
    if difficulty:
        filters += " AND difficulty = %s"
        params.append(difficulty)
    limit_filter = " ORDER BY name LIMIT %s OFFSET %s"
    params.extend([limit, (page - 1) * limit])

    async with conn.transaction():
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute(query+filters+limit_filter, (*params,))    
            exercises = await cursor.fetchall()
            await cursor.execute("SELECT COUNT(*) FROM exercises WHERE 1=1"+filters, (*params[:-2],))
            total = (await cursor.fetchone())['count']
    
    return exercises, total


async def get_exercise(conn, exercise_id):
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        await cursor.execute("SELECT * FROM exercises WHERE id = %s", (exercise_id,))
        res = await cursor.fetchone()
    return res


async def create_exercise(conn, exercise):
    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO exercises (name, description, muscle_group, equipment, difficulty) VALUES (%s, %s, %s, %s, %s) RETURNING id", (exercise.name, exercise.description, exercise.muscle_group, exercise.equipment or [], exercise.difficulty))
        res = await cursor.fetchone()
    return res


async def update_exercise(conn, exercise_id, exercise):
    async with conn.cursor() as cursor:
        await cursor.execute(
            """UPDATE exercises SET 
                    description = COALESCE(%s, description), 
                    equipment = COALESCE(%s, equipment), 
                    difficulty = COALESCE(%s, difficulty), 
                    muscle_group = COALESCE(%s, muscle_group) 
                WHERE id = %s RETURNING id
            """, (exercise.description, exercise.equipment or [], exercise.difficulty, exercise.muscle_group, exercise_id))
        res = await cursor.fetchone()
    return res


async def delete_exercise(conn, exercise_id):
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM exercises WHERE id = %s", (exercise_id,))
    if cursor.rowcount:
        return cursor.rowcount
    return None 
    