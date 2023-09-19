from datetime import timedelta, datetime

import bcrypt
import jwt

from passlib.hash import bcrypt
from bcrypt import hashpw, gensalt
from fastapi import APIRouter, HTTPException
from auth.models import RegisterUser, User, LoginUser
from mongo.connectMongo import connect_mongo

router = APIRouter()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

db = connect_mongo()
collection = db['users']


# Генерация токена доступа
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
async def register(user: RegisterUser):
    existing_user = collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already taken")
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')
    user_data = User(name=user.name, email=user.email, password=hashed_password, phone=user.phone, role="user")
    collection.insert_one(user_data.dict())
    return {"message": "Registration successful"}


@router.post("/login")
async def login(user: LoginUser, ACCESS_TOKEN_EXPIRE_MINUTES=10):
    check_email = collection.find_one({"email": user.email})

    if check_email is None:
        raise HTTPException(status_code=401, detail="Email not found")

    if not bcrypt.verify(user.password, check_email["password"]):
        raise HTTPException(status_code=400, detail="Bad data")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Возвращаем токен клиенту
    response = {"access_token": access_token, "token_type": "bearer"}
    return response
    # # Проверяем введенный пароль с хешем пароля из базы данных
    # if checkpw(credentials.password.encode('utf-8'), user["password"].encode('utf-8')):
    #     access_token = create_jwt_token({"sub": user["username"], "role": user["role"]})
    #     return {"access_token": access_token, "token_type": "bearer"}
    # else:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
