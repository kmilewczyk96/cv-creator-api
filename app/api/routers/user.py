import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.schemas.user import (
    EmailVerifiedResponse,
    Token,
    UserCreate,
    UserCreateResponse,
)
from core.db import SessionDep
from core.models import User
from services.token_service import TokenService
from services.verification_service import VerificationService

password_hash = PasswordHash.recommended()

user_router = APIRouter(
    prefix='/user',
)

@user_router.post(
    path='/create/',
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['user'],
)
async def create_user(user: UserCreate, session: SessionDep) -> JSONResponse:
    """Create a new user in the DB."""
    if user.password_1 != user.password_2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match!"
        )

    vs = VerificationService(session=session)
    verification_code = vs.generate_new_verification_code()
    new_user = User.model_validate(
        user,
        update={
            'hashed_password': password_hash.hash(user.password_1),
            'created': datetime.datetime.now(),
        }
    )
    new_user.verification_code_id = verification_code.id
    session.add(instance=new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )

    session.refresh(instance=new_user)
    vs.send_verification_code(verification_code=verification_code)
    return JSONResponse(
        content={
            'email': new_user.email,
            'full_name': new_user.full_name
        },
        status_code=201,
    )


@user_router.post(path='/token/', tags=['user'])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    ts = TokenService(session=session)
    user = ts.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect!"
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email is not verified!'
        )

    token = ts.create_token(user_email=user.email,)
    return Token(token_value=token, token_type='bearer')


@user_router.post(path='/verify-email/', tags=['user'])
async def verify_email(email: EmailStr, verification_code: str, session: SessionDep) -> EmailVerifiedResponse:
    vs = VerificationService(session=session)
    vs.verify_email(email=email, code=verification_code)
    return EmailVerifiedResponse(message='Successfully verified email!')
