
import base64

import pytest
from src.auth_lib.main import generate_salt, generate_token, hash_password, verify_password


def test_gen_salt():
    salt = generate_salt()
    try:
        decoded = base64.b64decode(salt)  # Should decode without error
        # Ensure it's originally 16 bytes before encoding
        assert len(decoded) == 16
    except Exception:
        pytest.fail("Salt is not a valid Base64-encoded string")
    salt2 = generate_salt()
    assert salt != salt2


def test_hash_and_verify_password():
    password = "secretihope"

    hashed_password = hash_password(password)

    assert hashed_password.startswith("$2b$")

    hashed_password_again = hash_password(password)

    assert hashed_password != hashed_password_again

    assert verify_password(password, hashed_password)


def test_create_and_verify_token():
    sub = "123"
    email = "something@gmail.com"
    other = "somethingelse"

    token = generate_token(sub, email=email, other=other)

    assert token
