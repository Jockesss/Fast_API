from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    role: str


class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class LoginUser(BaseModel):
    email: str
    password: str

