import datetime
import os
from typing import Annotated

import jwt
from fastapi import (
    HTTPException,
    status,
)
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import EmailStr
from sqlmodel import select

from core.db import SessionDep
from core.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/token')
class TokenService:
    """Service for handling authorization and access tokens."""
    algorithm = os.environ.get('ALGORITHM')
    password_hash = PasswordHash.recommended()
    secret_key = os.environ.get('SECRET_KEY')

    def __init__(self, session: SessionDep):
        self.session = session

    def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Tries to find a User with the provided email and checks if passwords match.
        Returns User or None if authentication fails.
        """
        sql = select(User).where(User.email == email)
        user = self.session.exec(statement=sql).first()
        if not user:
            return None
        if not self.password_hash.verify(password=password, hash=user.hashed_password):
            return None
        return user

    def create_token(self, user_email: EmailStr):
        """Creates and returns a new JWT Token valid for 24 hours."""
        to_encode = {
            'sub': user_email,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Failed to validate credentials!',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(jwt=token, key=self.secret_key, algorithms=[self.algorithm])
            email = payload.get('sub')
            if not email:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        else:
            user = self.get_user(email)
            if not user:
                raise credentials_exception
            return user

    def get_user(self, email: EmailStr) -> User | None:
        sql = select(User).where(User.email == email)
        return self.session.exec(sql).first()
