from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import User
from auth import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(username: str, password: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "username": user.username}

@router.post("/login")
async def login(username: str, password: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"id": user.id, "username": user.username}
