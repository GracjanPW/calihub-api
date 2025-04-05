from fastapi import testclient
from src.backend.api_routers.equipment.modals import Equipment, ReturnEquipment, ReturnEquipmentAll
from src.main import app

client = testclient.TestClient(app)


def test_get_equipment_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    res = client.get("/api/equipment", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnEquipmentAll(**data)

    assert type(validated_data.data) == list


def test_get_equipment_query_ok():
    login_res = client.post("/api/auth/token", data={
        "username":"user@gmail.com",
        "password":"userpassword"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    access_token = data['access_token']
    token_type = data['token_type']

    res = client.get("/api/equipment?search=back", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnEquipmentAll(**data)

    assert type(validated_data.data) == list


def test_get_equipment_ok():
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
    res = client.get(f"/api/equipment/{id}", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnEquipment(**data)

    assert type(validated_data.data) == Equipment


def test_create_equipment_ok():
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
    res = client.post("/api/equipment", json=data, headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 201
    

def test_update_equipment_ok():
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
    res = client.put(f"/api/equipment/{id}", json=data, headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200


def test_delete_equipment_ok():
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
    res = client.delete(f"/api/equipment/{id}", headers={"Authorization":f"{token_type} {access_token}"})

    assert res.status_code == 200