import os
from contextlib import asynccontextmanager

import resend
from fastapi import FastAPI
from fastapi.security import (
    OAuth2PasswordBearer,
)

from api.routers import user_router


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    yield

resend.api_key = os.environ.get('RESEND_API_KEY')

api = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
api.include_router(user_router)

@api.post('/user/auth/send-verification/')
async def send_verification_code():
    """
    Send an email with a new verification code to the logged-in User.
    :return:
    """
    params: resend.Emails.SendParams = {
        'from': f'noreply@{os.environ.get('DOMAIN_NAME')}',
        'to': [],
        'subject': 'Verification Code',
        'html': '<h2>Hola</h2>',
    }
    return resend.Emails.send(params)
