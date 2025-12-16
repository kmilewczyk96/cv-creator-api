from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    email: str
    password_1: str
    password_2: str
