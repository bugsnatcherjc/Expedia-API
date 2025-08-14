from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import schemas
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user)

@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, credentials)
    