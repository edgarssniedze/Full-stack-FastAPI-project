from fastapi import APIRouter, Depends
from sqlmodel import select
from app.core.security import get_current_user

users = APIRouter(tags=["User"])

@users.get(
        "/me",
        summary="Accesses the user's own account",
        description="Authorizes the current user with a JWT",
        response_description="User's account details with a hashed password")
async def get_me(curr_user=Depends(get_current_user)):
    return curr_user
