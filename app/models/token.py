from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class PasswordResetToken(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    token: str
    expires_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    userid: str | None = None


