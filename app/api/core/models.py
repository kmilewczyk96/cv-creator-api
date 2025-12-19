import uuid

from pydantic import EmailStr
from sqlmodel import (
    Column,
    Field,
    JSON,
    Relationship,
    SQLModel,
)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(default='', max_length=255)

    is_superuser: bool = False
    is_verified: bool = False


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    resumes: list['Resume'] = Relationship(back_populates='owner', cascade_delete=True)


class ResumeBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    structure: dict = Field(sa_column=Column(JSON))


class Resume(ResumeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, ondelete='CASCADE')
    owner: User | None = Relationship(back_populates='resumes')
