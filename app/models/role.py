from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.user import User

def date():
    return datetime.now(timezone.utc)

class Role(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str
    description: str
    users: list["User"] = Relationship(back_populates="role")

    created: datetime | None = None
    updated: datetime | None = None
    SQLModel.model_rebuild()
