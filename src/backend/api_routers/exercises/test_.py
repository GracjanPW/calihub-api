from fastapi import testclient
from src.backend.api_routers.exercises.modals import Exercise, ReturnExercise, ReturnExerciseId, ReturnExercises
from src.main import app

client = testclient.TestClient(app)


def test_get_exercises_ok():
    response = client.get("/api/exercises")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list
    assert valid.total >= 10


def test_get_exercises_ok_search():
    response = client.get("/api/exercises?search=bench%press")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list
    assert valid.total < 10


def test_get_exercises_ok_page_limit():
    limit = 10
    response1 = client.get(f"/api/exercises?limit={limit}&page=1")
    response2 = client.get(f"/api/exercises?limit={limit}&page=2")
    json1 = response1.json()
    valid1 = ReturnExercises(**json1)
    json2 = response2.json()
    valid2 = ReturnExercises(**json2)
    assert len(valid1.data) == limit
    assert valid1.data[0] != valid2.data[0]


def test_get_exercise_ok():
    exercise_id = 1
    response = client.get(f"/api/exercises/{exercise_id}")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercise(**json)
    assert type(valid.data) == Exercise
    assert valid.data.id == exercise_id


def test_get_exercise_fail_not_found():
    exercise_id = 200
    response = client.get(f"/api/exercises/{exercise_id}")
    json = response.json()
    assert response.status_code == 404
    assert json['message'] == 'Exercise not found'


def test_post_exercise_ok():
    exercise = {
        "name": "Deadlift Press",
        "description":"test exercise",
        "muscle_groups": [1],
        "equipment":[4],
        "difficulty": "novice"
    }
    response = client.post("/api/exercises", json=exercise)
    assert response.status_code == 201
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert type(valid.id) == int


def test_post_exercise_fail_invalid_input():
    exercise = {
        "name": "Deadlift Press",
    }
    response = client.post("/api/exercises", json=exercise)
    assert response.status_code == 422

def test_post_exercise_fail_invalid_equipment():
    exercise = {
        "name": "Deadlift Press",
        "description":"test exercise",
        "muscle_groups": [1],
        "equipment":[200],
        "difficulty": "novice"
    }
    response = client.post("/api/exercises", json=exercise)
    assert response.status_code == 400

def test_update_exercise_ok():
    exercise_id = 1
    exercise = {
        "difficulty": "intermediate",
        "description": "test desc",
        "muscle_groups": [2,5],
        "equipment": [1,6]
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
