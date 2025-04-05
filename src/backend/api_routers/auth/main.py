from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import psycopg
from src.backend.auth_lib.main import generate_salt, generate_token, get_current_user, hash_password, is_admin, verify_password
from src.backend.db import get_db
from pydantic import BaseModel


router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str


@router.get("/whoami")
async def check_authed_user(user=Depends(get_current_user)):
    return user

@router.get("/admin/token")
async def get_admin_token(user=Depends(get_current_user), is_admin=Depends(is_admin)):
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@router.post("/token", status_code=status.HTTP_200_OK)
async def sign_in(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn=Depends(get_db)):
    if form_data.username:
        async with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            await cursor.execute("SELECT id, email, role, hashed_password, quota FROM users WHERE email = %s", (form_data.username,))
            user = await cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        hashed_password = user["hashed_password"].decode() if isinstance(
            user["hashed_password"], bytes) else user["hashed_password"]

        if not verify_password(form_data.password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = generate_token(
            sub   = user['id'], 
            email = user['email'], 
            role  = user['role'], 
            quota = user['quota']
        ,)

        response.status_code = 200
        response.headers.append("Cache-Control","no-store")
        
        return {"access_token": access_token, "token_type": "Bearer"}

    response.status_code = 400
    return {"error": "invalid_request"}

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
