import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import (
    Session,
    create_engine,
)

db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
