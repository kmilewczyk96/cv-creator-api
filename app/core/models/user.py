import datetime
import uuid

from typing import Optional, TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)


if TYPE_CHECKING:
    from . import VerificationCode


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)

    full_name: str = Field(default='', max_length=255)
    hashed_password: str
    is_superuser: bool = False
    is_verified: bool = False

    created: datetime.datetime

    verification_code_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key='verificationcode.id',
        ondelete='SET NULL',
    )
    verification_code: Optional['VerificationCode'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={'uselist': False}
    )
