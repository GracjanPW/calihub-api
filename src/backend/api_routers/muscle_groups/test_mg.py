from fastapi import testclient
from src.backend.api_routers.muscle_groups.modals import MuscleGroup, ReturnMuscleGroup, ReturnMuscleGroups
from src.main import app

client = testclient.TestClient(app)


def test_get_muscle_groups_ok():
    res = client.get("/api/muscle_groups")

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnMuscleGroups(**data)

    assert type(validated_data.data) == list


def test_get_muscle_groups_query_ok():
    res = client.get("/api/muscle_groups?search=back")

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnMuscleGroups(**data)

    assert type(validated_data.data) == list


def test_get_muscle_group_ok():
    id = 1
    res = client.get(f"/api/muscle_groups/{id}")

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnMuscleGroup(**data)

    assert type(validated_data.data) == MuscleGroup


def test_create_muscle_group_ok():
    data = {
        "name": "test_group"
    }
    res = client.post("/api/muscle_groups", json=data)

    assert res.status_code == 201
    

def test_update_muscle_group_ok():
    id   = 1
    data = {
        "name": "test_group"
    }
    res = client.put(f"/api/muscle_groups/{id}", json=data)

    assert res.status_code == 200


def test_delete_muscle_group_ok():
    id = 1
    res = client.delete(f"/api/muscle_groups/{id}")

    assert res.status_code == 200