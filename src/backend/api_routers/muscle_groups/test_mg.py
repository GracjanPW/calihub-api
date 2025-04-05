from fastapi import testclient
from src.backend.api_routers.muscle_groups.modals import MuscleGroup, ReturnMuscleGroup, ReturnMuscleGroups
from src.main import app

client = testclient.TestClient(app)


def test_get_muscle_groups_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    res = client.get("/api/muscle_groups", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnMuscleGroups(**data)

    assert type(validated_data.data) == list


def test_get_muscle_groups_query_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    res = client.get("/api/muscle_groups?search=back", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnMuscleGroups(**data)

    assert type(validated_data.data) == list


def test_get_muscle_group_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    id = 1
    res = client.get(f"/api/muscle_groups/{id}", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnMuscleGroup(**data)

    assert type(validated_data.data) == MuscleGroup


def test_create_muscle_group_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    data = {
        "name": "test_group"
    }
    res = client.post("/api/muscle_groups", json=data, headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 201
    

def test_update_muscle_group_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    id   = 1
    data = {
        "name": "test_group"
    }
    res = client.put(f"/api/muscle_groups/{id}", json=data, headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200


def test_delete_muscle_group_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"admin@gmail.com",
        "password":"adminpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    id = 1
    res = client.delete(f"/api/muscle_groups/{id}", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200