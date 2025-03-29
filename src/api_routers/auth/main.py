from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
import psycopg
from src.auth_lib.main import generate_salt, generate_token, get_current_user, hash_password, verify_password
from src.db import get_db
from pydantic import BaseModel


router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str


@router.get("/whoami")
async def check_authed_user(user=Depends(get_current_user)):
    return user


@router.post("/token", status_code=status.HTTP_200_OK)
async def sign_in(response: Response, conn=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        await cursor.execute("SELECT id, email, hashed_password FROM users WHERE email = %s", (form_data.username,))
        user = await cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_password = user["hashed_password"].decode() if isinstance(
        user["hashed_password"], bytes) else user["hashed_password"]

    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = generate_token(user['id'], email=user['email'])

    # TODO: need to check how andif i need to add SameSite=Lax or Strict
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
    )
    response.status_code = 200
    return response


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def sign_up(newUser: UserCreate, conn=Depends(get_db)):
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (newUser.email,))
        count = (await cursor.fetchall())[0][0]

        if count > 0:
            raise HTTPException(
                status_code=400, detail="Email already taken, try logging in")

    hashed_password = hash_password(newUser.password)

    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO users (email, hashed_password) VALUES (%s, %s) RETURNING id", (newUser.email, hashed_password,))

    return {"message", "Account created successfully"}
