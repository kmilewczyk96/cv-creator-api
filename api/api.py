from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.security import OAuth2PasswordBearer

from api.schemas import UserCreate

api = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@api.get("/cv/list/")
async def get_cv_list(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the list of all CVs in the DB."""
    return {'token': token}


@api.post('/user/create/')
async def create_user(user: UserCreate):
    """Create a new user in the DB."""
    pass
