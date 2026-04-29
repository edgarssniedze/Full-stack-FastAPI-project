import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from app.core.config import expire_min, secret_key, algorithm


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