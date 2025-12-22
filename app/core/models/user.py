import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import (
    Field,
    SQLModel,
)


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)

    full_name: str = Field(default='', max_length=255)
    hashed_password: str
    is_superuser: bool = False
    is_verified: bool = False

    created: datetime.datetime
