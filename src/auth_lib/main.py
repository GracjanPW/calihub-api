import base64
import hashlib
import os
from passlib.hash import bcrypt


def generate_salt() -> str:
    return base64.b64encode(os.urandom(16)).decode('utf-8')


def hash_password(password: str, salt: str) -> str:
    salted_password = password+salt
    sha256_hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return bcrypt.hash(sha256_hashed)


def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    salted_password = plain_password + salt
    sha256_hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return bcrypt.verify(sha256_hashed, hashed_password)
