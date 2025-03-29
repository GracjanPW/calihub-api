import os
import subprocess
from fastapi.testclient import TestClient
import pytest

from src.main import app

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def reset_db():
    """Reset the database before the test session starts."""

    # You can run your script here, or execute any other commands that reset the database
    # Example: Running a shell command to reset the database
    script_path = os.path.join(os.path.dirname(
        __file__), "../scripts/db_dev.py")
    subprocess.run(["python", script_path], check=True)
    print("db reset")
    # Or if you are directly resetting it using SQL commands:
    # db_connection.execute("DELETE FROM users;")  # Just an example
    yield
    # Optionally, do cleanup after all tests are done
    subprocess.run(["python", script_path], check=True)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
