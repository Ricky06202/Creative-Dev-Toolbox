from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import RegexFavorite, PaletteFavorite, QuoteFavorite, DataFavorite

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/regex")
async def save_regex_favorite(favorite: RegexFavorite, session: Session = Depends(get_session)):
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite

@router.get("/regex/{user_id}")
async def get_regex_favorites(user_id: int, session: Session = Depends(get_session)):
    statement = select(RegexFavorite).where(RegexFavorite.user_id == user_id)
    return session.exec(statement).all()

@router.post("/palette")
async def save_palette_favorite(favorite: PaletteFavorite, session: Session = Depends(get_session)):
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite

@router.get("/palette/{user_id}")
async def get_palette_favorites(user_id: int, session: Session = Depends(get_session)):
    statement = select(PaletteFavorite).where(PaletteFavorite.user_id == user_id)
    return session.exec(statement).all()

@router.post("/quote")
async def save_quote_favorite(favorite: QuoteFavorite, session: Session = Depends(get_session)):
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite

@router.get("/quote/{user_id}")
async def get_quote_favorites(user_id: int, session: Session = Depends(get_session)):
    statement = select(QuoteFavorite).where(QuoteFavorite.user_id == user_id)
    return session.exec(statement).all()

@router.post("/data")
async def save_data_favorite(favorite: DataFavorite, session: Session = Depends(get_session)):
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite

@router.get("/data/{user_id}")
async def get_data_favorites(user_id: int, session: Session = Depends(get_session)):
    statement = select(DataFavorite).where(DataFavorite.user_id == user_id)
    return session.exec(statement).all()

@router.delete("/{fav_type}/{fav_id}")
async def delete_favorite(fav_type: str, fav_id: int, session: Session = Depends(get_session)):
    if fav_type == "regex":
        item = session.get(RegexFavorite, fav_id)
    elif fav_type == "palette":
        item = session.get(PaletteFavorite, fav_id)
    elif fav_type == "quote":
        item = session.get(QuoteFavorite, fav_id)
    elif fav_type == "data":
        item = session.get(DataFavorite, fav_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite type")
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(item)
    session.commit()
    return {"message": "Deleted successfully"}
