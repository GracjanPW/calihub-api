import os
import subprocess
from uuid import UUID
from fastapi import testclient
import pytest

from src.api_routers.exercises.modals import Exercise, ReturnExercise, ReturnExerciseId, ReturnExercises

from src.main import app

client = testclient.TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def reset_db():
    """Reset the database before the test session starts."""
    
    # You can run your script here, or execute any other commands that reset the database
    # Example: Running a shell command to reset the database
    script_path = os.path.join(os.path.dirname(__file__), "../../../scripts/db_dev.py")
    subprocess.run(["python", script_path], check=True)
    
    # Or if you are directly resetting it using SQL commands:
    # db_connection.execute("DELETE FROM users;")  # Just an example
    yield
    # Optionally, do cleanup after all tests are done


def test_get_exercises_ok():
    response = client.get("/api/exercises")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list

def test_get_exercise_ok():
    exercise_id = '52907d76-ab43-49a5-9f3f-4815f9f8fa78'
    response = client.get(f"/api/exercises/{exercise_id}")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercise(**json)
    assert type(valid.data) == Exercise
    assert valid.data.id == UUID(exercise_id)

def test_get_exercise_fail_not_found():
    exercise_id = '52907d76-ab43-49a5-9f3f-4815f9f8fa79'
    response = client.get(f"/api/exercises/{exercise_id}")
    json = response.json()
    assert response.status_code == 404
    assert json['message'] == 'Exercise not found'

def test_post_exercise_ok():
    exercise = {
        "name": "Deadlift Press",
        "muscle_group": "Chest",
        "difficulty": 3
    }
    response = client.post("/api/exercises/", json=exercise)
    assert response.status_code == 201
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert type(valid.id) == UUID

def test_post_exercise_fail_invalid_input():
    exercise = {
        "name": "Deadlift Press",
    }
    response = client.post("/api/exercises/", json=exercise)
    assert response.status_code == 422
    
def test_update_exercise_ok():
    exercise_id = "52907d76-ab43-49a5-9f3f-4815f9f8fa78"
    exercise = {
        "difficulty": 3
    }
    response = client.put(f"/api/exercises/{exercise_id}", json=exercise)
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert valid.id == UUID(exercise_id)

def test_detete_exercise_ok():
    exercise_id = "52907d76-ab43-49a5-9f3f-4815f9f8fa78"
    response = client.delete(f"/api/exercises/{exercise_id}")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert valid.id == UUID(exercise_id)
