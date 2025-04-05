from fastapi import testclient
from src.backend.api_routers.exercises.modals import Exercise, ReturnExercise, ReturnExerciseId, ReturnExercises
from src.main import app

client = testclient.TestClient(app)


def test_get_exercises_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    response = client.get("/api/exercises", headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list
    assert valid.total >= 10


def test_get_exercises_ok_search():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    response = client.get("/api/exercises?search=bench%press", headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercises(**json)
    assert type(valid.data) == list
    assert valid.total < 10


def test_get_exercises_ok_page_limit():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    limit = 10
    response1 = client.get(f"/api/exercises?limit={limit}&page=1", headers={"Authorization":f"{token_type} {access_token}"})
    response2 = client.get(f"/api/exercises?limit={limit}&page=2", headers={"Authorization":f"{token_type} {access_token}"})
    json1 = response1.json()
    valid1 = ReturnExercises(**json1)
    json2 = response2.json()
    valid2 = ReturnExercises(**json2)
    assert len(valid1.data) == limit
    assert valid1.data[0] != valid2.data[0]


def test_get_exercise_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']
    
    exercise_id = 1
    response = client.get(f"/api/exercises/{exercise_id}", headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExercise(**json)
    assert type(valid.data) == Exercise
    assert valid.data.id == exercise_id


def test_get_exercise_fail_not_found():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    exercise_id = 200
    response = client.get(f"/api/exercises/{exercise_id}", headers={"Authorization":f"{token_type} {access_token}"})
    json = response.json()
    assert response.status_code == 404
    assert json['message'] == 'Exercise not found'


def test_post_exercise_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    exercise = {
        "name": "Deadlift Press",
        "description":"test exercise",
        "muscle_groups": [2],
        "equipment":[4],
        "difficulty": "novice"
    }
    response = client.post("/api/exercises", json=exercise, headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 201
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert type(valid.id) == int


def test_post_exercise_fail_invalid_input():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']
    

    exercise = {
        "name": "Deadlift Press",
    }
    response = client.post("/api/exercises", json=exercise, headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 422

def test_post_exercise_fail_invalid_equipment():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']
    
    exercise = {
        "name": "Deadlift Press",
        "description":"test exercise",
        "muscle_groups": [2],
        "equipment":[200],
        "difficulty": "novice"
    }
    response = client.post("/api/exercises", json=exercise, headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 400

def test_update_exercise_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']
    
    exercise_id = 1
    exercise = {
        "difficulty": "intermediate",
        "description": "test desc",
        "muscle_groups": [2,5],
        "equipment": [2,6]
    }
    response = client.put(f"/api/exercises/{exercise_id}", json=exercise, headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert valid.id == exercise_id


def test_detete_exercise_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']
    
    exercise_id = 1
    response = client.delete(f"/api/exercises/{exercise_id}", headers={"Authorization":f"{token_type} {access_token}"})
    assert response.status_code == 200
    json = response.json()
    valid = ReturnExerciseId(**json)
    assert valid.id == exercise_id
