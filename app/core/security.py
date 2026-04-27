import jwt
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from app.database.db import SessionDep
from sqlmodel import select, or_
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
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
    print(token)
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except Exception as e:
        print("JWT ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
def get_user_by_id(user_id: UUID, session: SessionDep):
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()
    
    return UserPublic.model_validate(user)
    
def get_current_user(request: Request, session: SessionDep):
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def role_check(role: str):
    def check(user=Depends(get_current_user)):
        if role not in user["role"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return check