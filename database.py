from fastapi import  Depends
from sqlmodel import  Session, SQLModel, create_engine
from typing import Annotated
import os


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/form_builder")
connect_args = {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def create_db_and_tables():
    # SQLModel.metadata.drop_all(engine) 
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
