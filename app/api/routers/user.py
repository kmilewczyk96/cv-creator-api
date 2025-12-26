import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.schemas.user import (
    UserCreate,
    UserCreateResponse,
)
from core.db import SessionDep
from core.models import User
from services.verification_service import VerificationService

password_hash = PasswordHash.recommended()

user_router = APIRouter(
    prefix='/user',
)

@user_router.post(
    path='/create/',
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
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
