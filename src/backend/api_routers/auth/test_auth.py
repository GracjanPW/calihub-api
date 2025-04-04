from fastapi import testclient
import pytest
from src.main import app

client = testclient.TestClient(app)

user_register = {
    "email": "example@email.com",
    "password": "secret"
}
user_login = {
    "username": "example@email.com",
    "password": "secret"
}


def test_login_fail_user_doesnt_exist():
    login_res = client.post("/api/auth/token", data=user_login)
    assert login_res.status_code == 401
    data = login_res.json()
    assert "access_token" not in data


def test_not_authed():
    res = client.get("/api/auth/whoami")
    assert res.status_code == 401


def test_register_ok():
    res = client.post("/api/auth/register", json=user_register)
    json = res.json()
    assert res.status_code == 201
    assert "message" in json


def test_register_fail():
    res = client.post("/api/auth/register", json=user_register)
    json = res.json()
    assert res.status_code == 400
    assert "detail" in json


def test_login():
    login_res = client.post("/api/auth/token", data=user_login)
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data

    access_token = data['access_token']
    token_type = data['token_type']
    # client.cookies.set("access_token", login_res.cookies["access_token"])
    whoami_res = client.get("/api/auth/whoami", headers={"Authorization":f"{token_type} {access_token}"})
    whoami_json = whoami_res.json()
    print(whoami_json)
    assert whoami_res.status_code == 200
    assert "sub" in whoami_json
    assert whoami_json['email'] == user_login['username']


def test_login_fail_user_exists():
    user_login_false = {
        "username": user_login['username'],
        "password": "wrongorsomthing"
    }
    login_res = client.post("/api/auth/token", data=user_login_false)
    assert login_res.status_code == 401
    assert "access_token" not in login_res.cookies
