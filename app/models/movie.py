from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

def date():
    return datetime.now(timezone.utc)

class Movie(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    title: str
    description: str
    year: int
    price: Decimal = Field(decimal_places=2)
    created: datetime = Field(default_factory=date)
    updated: datetime | None = None 

class MoviePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    year: int
    price: Decimal
    created: datetime

class MovieCreate(BaseModel):
    title: str
    description: str
    year: int
    price: Decimal = Field(decimal_places=2)

class MovieUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    year: int | None = None
    price: Decimal | None = None

class MoviesPublic(SQLModel):
    data: list[MoviePublic]
    count: int
 