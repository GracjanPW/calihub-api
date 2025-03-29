from fastapi import testclient
from src.main import app

client = testclient.TestClient(app)

def test_register():
    user = {
        "email":"example@email.com",
        "password":"secret"
    }
    res = client.post("/api/auth/register",json=user)
    json = res.json()
    assert res.status_code == 201
    assert "message" in json

    user2 = {
        "email":"example@email.com",
        "password":"secret123"
    }
    res = client.post("/api/auth/register",json=user)
    json = res.json()
    assert res.status_code == 400
    assert "detail" in json
