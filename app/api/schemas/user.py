from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password_1: str
    password_2: str


class UserCreateResponse(BaseModel):
    email: EmailStr
    full_name: str
