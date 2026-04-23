from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from app.models.NtoN import UserRole

if TYPE_CHECKING:
    from app.models.role import Role


def date():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    username: str
    email: str = Field(index=True, unique=True)
    hashed_password: str

    roles: List["Role"] = Relationship(
        back_populates="users",
        link_model=UserRole
    )

    created: datetime = Field(default_factory=date)
    updated: datetime | None = None

class UserReg(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserPublic(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created: datetime
    updated: datetime | None = None

