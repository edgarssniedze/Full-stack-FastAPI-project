from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, or_

from app.database.db import SessionDep
from app.models.token import Token
from app.models.user import User, UserReg, UserPublic
from app.core.security import hash_password, verify_password, create_jwt

auth = APIRouter(tags=["Authentication"], prefix="/api")
 
@auth.post("/register", 
           summary="Registers a new user",
           description="Creates a new user account",
           response_description="User's UUID and e-mail",
           response_model=UserPublic)
def register(user_data: UserReg, session: SessionDep):
    
    existing_email = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already in use")

    user = User(
        email=user_data.email,
        username= user_data.username,
        hashed_password=hash_password(user_data.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@auth.post("/login", 
           summary="Login an user into their account",
           description="Signs an user in using their account details",
           response_description="User's JW token",
           response_model=Token)
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    
    existing_user = session.exec(
        select(User).where(or_(User.email == form_data.username, User.username == form_data.username))
    ).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(form_data.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt({"sub": str(existing_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

