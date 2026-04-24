from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.models.NtoN import UserRole

if TYPE_CHECKING:
    from app.models.user import User

def date():
    return datetime.now(timezone.utc)

class Role(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str
    description: str

    created: datetime = Field(default_factory=date)
    updated: datetime | None = None

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole
    )

from sqlmodel import SQLModel

SQLModel.model_rebuild()