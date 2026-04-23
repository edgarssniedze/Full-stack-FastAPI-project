import jwt
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database.db import SessionDep
from sqlmodel import select
from uuid import UUID
from app.models.user import User, UserPublic
from dotenv import load_dotenv
import os

load_dotenv()

def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

expire_min = int(get_env("ACCESS_TOKEN_EXPIRE_MIN", "30"))
secret_key = get_env("SECRET_KEY")
algorithm = get_env("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(plain_pass: str, hashed_pass):
    return password_hash.verify(plain_pass, hashed_pass)

def create_jwt(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_min)

    to_encode.update({
        "exp":expire
    })

    token = jwt.encode(to_encode, secret_key, algorithm)

    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> UserPublic:
    try:
        payload = decode_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid credentials")
 
        userid = payload.get("sub")

    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = session.exec(
        select(User).where(User.id == UUID(userid))        
    ).first()
    
    if not user:    
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    userdata = User(
        id = user.id,
        username = user.username,
        email = user.email,
        creation_date = user.created,
    )

    return userdata