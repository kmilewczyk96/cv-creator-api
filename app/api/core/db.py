import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
)

db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)

def create_db_and_tables():
    from api.core.models import User, Resume
    print(f"Creating tables for models: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
