import os
import subprocess
from uuid import UUID
from fastapi import testclient
import pytest

from src.api_routers.exercises.modals import Exercise, ReturnExercise, ReturnExerciseId, ReturnExercises

from src.main import app

client = testclient.TestClient(app)


def test_get_exercises_ok():
    response = client.get("/api/exercises")
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list
    assert valid.total > 10

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
