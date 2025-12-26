import os
from contextlib import asynccontextmanager

import resend
from fastapi import FastAPI

from api.routers import user_router


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    yield

resend.api_key = os.environ.get('RESEND_API_KEY')

api = FastAPI(lifespan=lifespan)
api.include_router(user_router)
