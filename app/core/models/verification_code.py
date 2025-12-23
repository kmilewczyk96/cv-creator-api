import datetime
import uuid
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from . import User


class VerificationCode(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    code: str

    created: datetime.datetime
    expires: datetime.datetime

    user: 'User' = Relationship(
        back_populates='verificationcode',
        sa_relationship_kwargs={'uselist': False}
    )
