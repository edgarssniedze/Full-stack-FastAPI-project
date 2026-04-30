from fastapi import APIRouter, HTTPException, Depends, Form, Response
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from sqlmodel import select, or_
from app.core.security import hash_password

from app.database.db import SessionDep
from app.models.token import PasswordResetToken
from app.models.user import User
from app.database.db import SessionDep
from app.core.services import get_role_by_name, get_current_user
from secrets import token_urlsafe
import smtplib
from email.mime.text import MIMEText

reset = APIRouter(tags=["Reset links"], prefix="/help")

@reset.post("/changepassword")    
async def reset_password(session: SessionDep, user=Depends(get_current_user)):

    token = token_urlsafe(32)

    reset_entry = PasswordResetToken(
        user_id = user.id,
        token = token,
        expires_at = datetime.now() + timedelta(hours=1)
    )

    session.add(reset_entry)
    session.commit()

    reset_link = f"http://localhost:8000/passwordreset?token={token}"

    msg = MIMEText(f"Click here: {reset_link}")
    msg["Subject"] = "Password Reset Pending"
    msg["From"] = "sender@example.com"
    msg["To"] = "receiver@example.com"
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)

    return RedirectResponse(url="/profile", status_code=301)

@reset.post("/changeemail")    
async def change_email(session: SessionDep, user=Depends(get_current_user)):
    token = token_urlsafe(32)

    reset_entry = PasswordResetToken(
    user_id = user.id,
        token = token,
        expires_at = datetime.now() + timedelta(hours=1)
    )

    session.add(reset_entry)
    session.commit()

    reset_link = f"http://localhost:8000/emailreset?token={token}"

    msg = MIMEText(f"Click here: {reset_link}")
    msg["Subject"] = "Email Reset pending"
    msg["From"] = "sender@example.com"
    msg["To"] = "receiver@example.com"
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)
    return RedirectResponse(url="/profile", status_code=301)

@reset.post("/passwordreset")
async def pass_reset_form(
    session: SessionDep,
    token: str = Form(...),
    new_password: str = Form(...),
):
    reset_entry = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token
        )
    ).first()

    if not reset_entry:
        raise HTTPException(status_code=400, detail="Invalid token")
    if reset_entry.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired")

    user = session.get(User, reset_entry.user_id)

    user.hashed_password = hash_password(new_password)

    session.delete(reset_entry)

    session.add(user)
    session.commit()

    return RedirectResponse(url="/login", status_code=301)

@reset.post("/emailreset")
async def email_reset_form(
    session: SessionDep,
    token: str = Form(...),
    new_email: str = Form(...),
):
    reset_entry = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token
        )
    ).first()

    if not reset_entry:
        raise HTTPException(status_code=400, detail="Invalid token")
    if reset_entry.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired")

    user = session.get(User, reset_entry.user_id)

    user.email = new_email

    session.delete(reset_entry)

    session.add(user)
    session.commit()

    return RedirectResponse(url="/login", status_code=301)

