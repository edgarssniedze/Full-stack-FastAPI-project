from fastapi import Request, Depends, HTTPException
from app.database.db import SessionDep
from sqlmodel import select
from uuid import UUID
from app.models.user import User, UserPublic
from app.models.role import Role

def to_user_public(user: User) -> UserPublic:
    return UserPublic(
        id=user.id,
        email=user.email,
        username=user.username,
        role=user.role.name if user.role else None,
        role_id=user.role_id,
        created=user.created,
    )

def get_user_by_id(user_id: UUID, session: SessionDep):
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()

    if not user:
        return None

    return to_user_public(user)

def get_current_user(request: Request, session: SessionDep):

    payload = request.state.user

    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def role_check(required_role: str):
    def checker(user=Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker

def get_role_by_name(name: str, session: SessionDep):
    return session.exec(
        select(Role).where(Role.name == name)
    ).first()