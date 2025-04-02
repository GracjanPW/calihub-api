from fastapi import testclient
from src.backend.api_routers.equipment.modals import Equipment, ReturnEquipment, ReturnEquipmentAll
from src.main import app

client = testclient.TestClient(app)


def test_get_equipment_ok():
    res = client.get("/api/equipment")

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnEquipmentAll(**data)

    assert type(validated_data.data) == list


def test_get_equipment_query_ok():
    res = client.get("/api/equipment?search=back")

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnEquipmentAll(**data)

    assert type(validated_data.data) == list


def test_get_equipment_ok():
    id = 1
    res = client.get(f"/api/equipment/{id}")

    assert res.status_code == 200

    data = res.json()
    validated_data = ReturnEquipment(**data)

    assert type(validated_data.data) == Equipment


def test_create_equipment_ok():
    data = {
        "name": "test_group"
    }
    res = client.post("/api/equipment", json=data)

    assert res.status_code == 201
    

def test_update_equipment_ok():
    id   = 1
    data = {
        "name": "test_group"
    }
    res = client.put(f"/api/equipment/{id}", json=data)

    assert res.status_code == 200


def test_delete_equipment_ok():
    id = 1
    res = client.delete(f"/api/equipment/{id}")

    assert res.status_code == 200