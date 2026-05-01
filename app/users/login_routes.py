from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.database import get_session
from app.models.models import User
from app.schemas.schemas import UserLogin
import bcrypt

router = APIRouter()

@router.post("/login")
def login_user(user_data: UserLogin, session: Session = Depends(get_session)):
    username = user_data.username
    password = user_data.password

    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }