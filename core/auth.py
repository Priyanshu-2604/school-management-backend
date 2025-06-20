# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.db.session import get_db
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully", "user_id": db_user.id}

@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }
