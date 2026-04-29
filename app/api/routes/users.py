from fastapi import APIRouter, Depends
from app.core.services import get_current_user

users = APIRouter(tags=["User"], prefix="/api")

@users.get(
        "/profile",
        summary="Accesses the user's own account",
        description="Authorizes the current user with a JWT",
        response_description="User's account details with a hashed password")
async def get_me(curr_user=Depends(get_current_user)):
    return curr_user

