import psycopg


async def get_exercises(conn):
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        await cursor.execute("SELECT * FROM exercises")
        res = await cursor.fetchall()
    return res


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
    