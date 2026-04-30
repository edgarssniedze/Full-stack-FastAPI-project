from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends
from app.core.seed import seed_roles
from app.models import movie, user, rental, role, token
from app.core.config import load_dotenv, get_env

database_url = get_env("DATABASE_URL")
engine = create_engine(database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print(f"HERE HERE HERE ----> {SQLModel.metadata.tables.keys()}")
    with Session(engine) as session:
        seed_roles(session)
    yield
    print("stopping")