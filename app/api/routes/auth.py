from fastapi import APIRouter, HTTPException, Depends, Form, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlmodel import select, or_

from app.database.db import SessionDep
from app.models.token import Token
from app.models.user import User, UserReg, UserPublic
from app.core.security import hash_password, verify_password, create_jwt

auth = APIRouter(tags=["Authentication"], prefix="/api")
 
# add 404 route

@auth.post("/register", 
           summary="Registers a new user",
           description="Creates a new user account",
           response_description="User's UUID and e-mail",
           response_model=UserPublic)
def register(session: SessionDep,
             username: str = Form(...),
             password: str = Form(...),
             email: str= Form(...)):
    
    existing_email = session.exec(
        select(User).where(User.email == email)
    ).first()

    existing_username = session.exec(
        select(User).where(User.username == username)
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already in use")

    user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@auth.post("/login", 
            summary="Login an user into their account",
            description="Signs an user in using their account details",
            response_description="User's JW token")
def login(session: SessionDep, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
        
    existing_user = session.exec(
        select(User).where(or_(User.email == form_data.username, User.username == form_data.username))
    ).first()   

    existing_user.roles
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, existing_user.hashed_password):
      raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt({
        "sub": str(existing_user.id),
        "role": [role.name for role in existing_user.roles]
    })
    
    response = RedirectResponse(url="/profile", status_code=301)

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,   
        samesite="lax",
        secure=False    
    )

    return response