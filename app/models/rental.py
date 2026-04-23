from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime, timezone

def date():
    return datetime.now(timezone.utc)

class Rental(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(foreign_key="user.id")
    movie_id: UUID = Field(foreign_key="movie.id")
    cost: float = Field(decimal_places=2)
    rented_at: datetime | None = None
    returned_at: datetime | None = None
    created: datetime = Field(default_factory=date)
    updated: datetime | None = None