
import base64

import pytest
from src.auth_lib.main import generate_salt


def test_gen_salt():
    salt = generate_salt()
    try:
        decoded = base64.b64decode(salt)  # Should decode without error
        assert len(decoded) == 16  # Ensure it's originally 16 bytes before encoding
    except Exception:
        pytest.fail("Salt is not a valid Base64-encoded string")
    salt2 = generate_salt()
    assert salt != salt2

