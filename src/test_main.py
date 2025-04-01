import os
import subprocess
from fastapi.testclient import TestClient
import pytest

from src.main import app

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def reset_db():
    """Reset the database before the test session starts, ensuring scripts run sequentially."""

    script_path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/db_dev.py"))
    script_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/db_seed.py"))

    def run_script(script_path):
        """Run a script and ensure it completes successfully before moving on."""
        print(f"🔄 Running {script_path}...")
        process = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"✅ {script_path} executed successfully:\n{process.stdout}")

    print("🔄 Resetting database...")

    # Run db_dev.py first, wait until it finishes, then run db_seed.py
    run_script(script_path1)  # Create schema
    run_script(script_path2)  # Seed data

    print("✅ Database reset completed.")

    yield  # Tests run after this point

    print("🔄 Resetting database after tests...")

    # Reset again after tests (optional)
    run_script(script_path1)
    run_script(script_path2)

    print("✅ Post-test database reset completed.")

def test_test():
    pass