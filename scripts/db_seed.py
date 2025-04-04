import asyncio
import os
from passlib.hash import bcrypt
import psycopg


DATABASE_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
}


DB_CONFIG = {
    'dbname': 'calihub_dev_db',
    'user':'app_user',
    'password':'devpassword',
    'host':'localhost',
    'port': 5432
}

SEED_DATA_MUSCLE_GROUPS = [
    {
        'id': 1,
        'name': 'Chest',
    },
    {
        'id': 2,
        'name': 'Back',
    },
    {
        'id': 3,
        'name': 'Shoulders',
    },
    {
        'id': 4,
        'name': 'Arms',
    },
    {
        'id': 5,
        'name': 'Core',
    },
    {
        'id': 6,
        'name': 'Legs',
    },
    {
        'id': 7,
        'name': 'Full Body',
    },
    {
        'id': 8,
        'name': 'Calves',
    },
    {
        'id': 9,
        'name': 'Glutes',
    },
    {
        'id': 10,
        'name': 'Biceps',
    },
    {
        'id': 11,
        'name': 'Triceps',
    },
    {
        'id': 12,
        'name': 'Forearms',
    },
    {
        'id': 13,
        'name': 'Lats',
    },
    {
        'id': 14,
        'name': 'Traps',
    },
    {
        'id': 15,
        'name': 'Obliques',
    }
]

SEED_DATA_EQUIPMENT = [
    {
        'id': 1,
        'name': 'Bodyweight',
    },
    {
        'id': 2,
        'name': 'Pull up bar',
    },
    {
        'id': 3,
        'name': 'Weight belt',
    },
    {
        'id': 4,
        'name': 'Resistance bands',
    },
    {
        'id': 5,
        'name': 'Dip bar',
    },
    {
        'id': 6,
        'name': 'Weight vest',
    },
    {
        'id': 7,
        'name': 'Parallettes',
    },
    {
        'id': 8,
        'name': 'Barbell',
    },
    {
        'id': 9,
        'name': 'Ladder'
    },
    {
        'id': 10,
        'name': 'Pole'
    }
]

SEED_DATA_EXERCISES = [
    {
        'name': 'Pushups',
        'description': 'A basic pushup exercise',
        'difficulty': 'beginner',
        'muscle_group': [1],
        'equipment': [1, 6],
    },
    {
        'name': 'Pull ups',
        'description': 'A basic pull up exercise',
        'difficulty': 'beginner',
        'muscle_group': [2],
        'equipment': [1, 2, 3, 6],
    },
    {
        'name': 'Squats',
        'description': 'A basic squat exercise',
        'difficulty': 'beginner',
        'muscle_group': [3],
        'equipment': [1, 6, 8],
    },
    {
        'name': 'Dips',
        'description': 'A calisthenic exercise that targets triceps and chest',
        'difficulty': 'intermediate',
        'muscle_group': [1, 4],
        'equipment': [5, 6],
    },
    {
        'name': 'Chin ups',
        'description': 'An exercise that works the back and biceps using an underhand grip',
        'difficulty': 'intermediate',
        'muscle_group': [2, 10],
        'equipment': [1, 2],
    },
    {
        'name': 'Leg raises',
        'description': 'An exercise for targeting the core and lower abs',
        'difficulty': 'intermediate',
        'muscle_group': [5],
        'equipment': [1],
    },
    {
        'name': 'Bodyweight Rows',
        'description': 'A horizontal pulling exercise for the back and biceps',
        'difficulty': 'beginner',
        'muscle_group': [2, 10],
        'equipment': [1, 7],
    },
    {
        'name': 'Handstand Pushups',
        'description': 'A challenging calisthenics exercise that targets shoulders and triceps',
        'difficulty': 'advanced',
        'muscle_group': [3],
        'equipment': [1],
    },
    {
        'name': 'Pistol Squats',
        'description': 'A one-legged squat exercise that targets the legs and core',
        'difficulty': 'advanced',
        'muscle_group': [6],
        'equipment': [1],
    },
    {
        'name': 'Lunges',
        'description': 'A lower-body exercise that targets the glutes, quads, and hamstrings',
        'difficulty': 'beginner',
        'muscle_group': [6],
        'equipment': [1],
    },
    {
        'name': 'Mountain Climbers',
        'description': 'A dynamic calisthenics exercise that targets core and legs',
        'difficulty': 'beginner',
        'muscle_group': [5, 6],
        'equipment': [1],
    },
    {
        'name': 'Plank',
        'description': 'A core strengthening exercise that works the abs, shoulders, and back',
        'difficulty': 'beginner',
        'muscle_group': [5],
        'equipment': [1],
    },
    {
        'name': 'Box Jumps',
        'description': 'A plyometric exercise for the legs and glutes',
        'difficulty': 'intermediate',
        'muscle_group': [6],
        'equipment': [8],
    },
    {
        'name': 'Burpees',
        'description': 'A full-body calisthenics exercise that targets the core, chest, and legs',
        'difficulty': 'intermediate',
        'muscle_group': [1, 5, 6],
        'equipment': [1],
    },
    {
        'name': 'Wall Sit',
        'description': 'An isometric exercise that targets the quads and glutes',
        'difficulty': 'beginner',
        'muscle_group': [6],
        'equipment': [1],
    },
    {
        'name': 'Tricep Dips',
        'description': 'A tricep-focused calisthenics exercise performed on parallel bars',
        'difficulty': 'intermediate',
        'muscle_group': [4],
        'equipment': [5],
    },
    {
        'name': 'Superman',
        'description': 'A bodyweight exercise targeting the lower back and glutes',
        'difficulty': 'beginner',
        'muscle_group': [6],
        'equipment': [1],
    },
    {
        'name': 'Plank to Pushup',
        'description': 'A core and upper-body exercise combining a plank with a push-up movement',
        'difficulty': 'intermediate',
        'muscle_group': [1, 5],
        'equipment': [1],
    },
    {
        'name': 'Tuck Jumps',
        'description': 'A high-intensity plyometric exercise for legs and glutes',
        'difficulty': 'advanced',
        'muscle_group': [6],
        'equipment': [1],
    },
    {
        'name': 'Hindu Pushups',
        'description': 'A dynamic pushup variation that targets the chest, shoulders, and core',
        'difficulty': 'intermediate',
        'muscle_group': [1, 3],
        'equipment': [1],
    },
    {
        'name': 'Bear Crawl',
        'description': 'A full-body movement that targets core, shoulders, and legs',
        'difficulty': 'intermediate',
        'muscle_group': [5, 6],
        'equipment': [1],
    },
    {
        'name': 'Back Lever',
        'description': 'An advanced calisthenics skill targeting the shoulders, back, and core. Holding the body parallel to the ground while hanging.',
        'difficulty': 'advanced',
        'muscle_group': [2, 5, 3],
        'equipment': [1, 2],
    },
    {
        'name': 'Front Lever',
        'description': 'An advanced calisthenics exercise that engages the core, back, and shoulders by holding the body parallel to the ground from a hanging position.',
        'difficulty': 'advanced',
        'muscle_group': [2, 5, 3],
        'equipment': [1, 2],
    },
    {
        'name': 'Human Flag',
        'description': 'A dynamic calisthenics skill where the body is held horizontally to a vertical pole, requiring immense core and shoulder strength.',
        'difficulty': 'advanced',
        'muscle_group': [2, 3, 4],
        'equipment': [1, 9, 10],
    },
    {
        'name': 'Muscle Up',
        'description': 'A challenging pull-up progression that requires the ability to transition from a pull-up into a dip, targeting back, shoulders, and arms.',
        'difficulty': 'advanced',
        'muscle_group': [2, 4, 3],
        'equipment': [1, 2],
    },
    {
        'name': 'L-Sit',
        'description': 'A core exercise where the legs are lifted and held in an "L" shape while seated, targeting the abs, hip flexors, and shoulders.',
        'difficulty': 'advanced',
        'muscle_group': [5, 3],
        'equipment': [1],
    },
    {
        'name': 'Handstand Walk',
        'description': 'An advanced calisthenics skill where the individual walks on their hands, requiring balance, shoulder stability, and core strength.',
        'difficulty': 'advanced',
        'muscle_group': [3, 5],
        'equipment': [1],
    },
    {
        'name': 'Dragon Flag',
        'description': 'An advanced core exercise where the body is raised in a straight line, supported only by the shoulders and head, requiring immense abdominal strength.',
        'difficulty': 'advanced',
        'muscle_group': [5, 2, 3],
        'equipment': [1],
    },
    {
        'name': 'Pistol Squats',
        'description': 'A single-leg squat that targets the quads, glutes, and core while requiring excellent balance and flexibility.',
        'difficulty': 'advanced',
        'muscle_group': [6],
        'equipment': [1],
    },
    {
        'name': 'V-Sit',
        'description': 'A core exercise where the legs are lifted and held in a "V" shape, targeting the abs and hip flexors.',
        'difficulty': 'intermediate',
        'muscle_group': [5],
        'equipment': [1],
    },
    {
        'name': 'Single Arm Pushups',
        'description': 'An advanced pushup variation where only one arm is used to perform the movement, targeting the chest, shoulders, and triceps.',
        'difficulty': 'advanced',
        'muscle_group': [1],
        'equipment': [1],
    }
]

import psycopg
from psycopg.rows import dict_row

async def seed():
    conn = await psycopg.AsyncConnection.connect(**DB_CONFIG)
    await conn.set_autocommit(True)
    async with conn.transaction():
        async with conn.cursor() as cursor: # ✅ Fix: Use `await conn.cursor()`
            # Insert admin user
            admin_password = "adminpassword"
            admin_hashed_password = bcrypt.hash(admin_password.encode())
            await cursor.execute(
                "INSERT INTO users (email, hashed_password, role) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING",
                ("admin@gmail.com", admin_hashed_password, "admin")
            )

            # Insert muscle groups
            await cursor.executemany(
                "INSERT INTO muscle_groups (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                [(item['id'], item['name']) for item in SEED_DATA_MUSCLE_GROUPS]
            )
            await cursor.execute(
                "SELECT setval('muscle_groups_id_seq', (SELECT MAX(id) FROM muscle_groups) + 1)"
            )

            # Insert equipment
            await cursor.executemany(
                "INSERT INTO equipment (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                [(item['id'], item['name']) for item in SEED_DATA_EQUIPMENT]
            )
            await cursor.execute(
                "SELECT setval('equipment_id_seq', (SELECT MAX(id) FROM equipment) + 1)"
            )

            # Insert exercises
            for exercise in SEED_DATA_EXERCISES:
                # Insert exercise data
                await cursor.execute(
                    "INSERT INTO exercises (name, description, difficulty) VALUES (%s, %s, %s) RETURNING id",
                    (exercise['name'], exercise['description'], exercise['difficulty'])
                )
                exercise_id = (await cursor.fetchone())[0]

                # Insert exercise-muscle group associations
                await cursor.executemany(
                    "INSERT INTO exercise_muscle_groups (exercise_id, muscle_group_id) VALUES (%s, %s)",
                    [(exercise_id, mg_id) for mg_id in exercise['muscle_group']]
                )

                # Insert exercise-equipment associations
                await cursor.executemany(
                    "INSERT INTO exercise_equipment (exercise_id, equipment_id) VALUES (%s, %s)",
                    [(exercise_id, eq_id) for eq_id in exercise['equipment']]
                )
            

    await conn.close()  # ✅ Always close the connection
    
if __name__ == "__main__":
    asyncio.run(seed())