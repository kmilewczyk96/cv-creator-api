from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.security import OAuth2PasswordBearer

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

api = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@api.get("/cv/list/alibaba/")
async def get_cv_list(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the list of all CVs in the DB."""
    return {'token': token}


@api.post('/user/create/')
async def create_user(user: UserCreate):
    """Create a new user in the DB."""
    pass
