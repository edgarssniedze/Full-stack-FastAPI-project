from sqlmodel import SQLModel, Field, Relationship, text
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.role import Role


def date():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    username: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    
    
    role_id: UUID = Field(default=None, foreign_key="role.id",
    )
    role: Role = Relationship(back_populates="users")
    created: datetime = Field(default_factory=date)
    updated: datetime | None = None

class UserReg(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role_id: UUID
    role: str
    username: str
    email: EmailStr
    created: datetime
    updated: datetime | None = None

