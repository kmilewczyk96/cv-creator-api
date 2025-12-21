import os
from contextlib import asynccontextmanager
from typing import Annotated, Dict

import resend
from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from api.core.db import create_db_and_tables
from api.core.models import (
    User,
    Resume
)
from api.schemas import UserCreate


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    create_db_and_tables()
    yield

resend.api_key = os.environ.get('RESEND_API_KEY')
api = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@api.get("/cv/list/")
async def get_cv_list(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the list of all CVs in the DB."""
    return {'token': token}


@api.post('/user/create/')
async def create_user(user: UserCreate):
    """Create a new user in the DB."""
    pass


@api.post('/email/send-email/')
def send_mail(recipient: EmailStr) -> Dict:
    params: resend.Emails.SendParams = {
        "from": "noreply@karol-milewczyk.com",
        "to": [recipient],
        "subject": "Hello World",
        "html": "<strong>it works!</strong>",
    }
    email: resend.Email = resend.Emails.send(params)
    return email
