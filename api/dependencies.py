# app/api/dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM
from app.db.models import User
from app.db.session import SessionLocal

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(required_roles: List[str]):
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_dependency
