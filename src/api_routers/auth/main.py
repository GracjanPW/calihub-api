from fastapi import APIRouter, Depends, HTTPException, status
from src.auth_lib.main import generate_salt, hash_password
from src.db import get_db
from pydantic import BaseModel


router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str


@router.post("/token")
async def sign_in(conn = Depends(get_db)):
    pass

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def sign_up(newUser:UserCreate ,conn = Depends(get_db)):
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (newUser.email,))
        count =(await cursor.fetchall())[0][0]
        
        if count > 0:
            raise HTTPException(status_code=400, detail="Email already taken, try logging in")
    
    salt = generate_salt()
    hashed_password = hash_password(newUser.password, salt)

    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO users (email, hashed_password, password_salt) VALUES (%s, %s, %s) RETURNING id", (newUser.email, hashed_password, salt,))
    
    return {"message", "Account created successfully"}
