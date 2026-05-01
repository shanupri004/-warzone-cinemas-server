# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.models import User
from app.schemas.schemas import UserCreate
import bcrypt

router = APIRouter()

@router.post("/register")
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check if username or email already exists
    existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create user object
    user = User(
        email=user_data.email,
        username=user_data.username,
        password=hashed_password,
        role="user"  # default role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
