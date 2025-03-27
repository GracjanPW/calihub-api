from fastapi import testclient

from .exercises import Exercise, ReturnExercise, ReturnExerciseId, ReturnExercises

from ..main import app

client = testclient.TestClient(app)

def test_get_exercises_ok():
    response = client.get("/api/exercises/")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list

def test_get_exercise_ok():
    exercise_id = 1
    response = client.get(f"/api/exercises/{exercise_id}")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercise(**json)
    assert type(valid.data) == Exercise
    assert valid.data.id == exercise_id

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
    assert type(valid.id) == int

def test_post_exercise_fail_invalid_input():
    exercise = {
        "name": "Deadlift Press",
    }
    response = client.post("/api/exercises/", json=exercise)
    assert response.status_code == 422
    
def test_update_exercise_ok():
    exercise_id = 1
    exercise = {
        "name": "Deadlift Press",
        "muscle_group": "Chest",
        "difficulty": 3
    }
    response = client.put(f"/api/exercises/{exercise_id}", json=exercise)
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert valid.id == exercise_id

def test_detete_exercise_ok():
    exercise_id = 1
    response = client.delete(f"/api/exercises/{exercise_id}")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert valid.id == exercise_id
