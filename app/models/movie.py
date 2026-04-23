from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

def date():
    return datetime.now(timezone.utc)

class Movie(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    title: str
    description: str
    year: int
    price: float = Field(decimal_places=2)
    created: datetime = Field(default_factory=date)
    updated: datetime | None = None 