from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from database import get_db
from models import User, UserFavorite, Player

router = APIRouter()

class TelegramAuthData(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None

@router.post("/auth")
async def authenticate_user(auth_data: TelegramAuthData, db: AsyncSession = Depends(get_db)):
    """Telegram üzerinden giriş yapan kullanıcıyı veritabanına kaydeder/günceller."""
    stmt = select(User).where(User.telegram_id == auth_data.telegram_id)
    user = (await db.execute(stmt)).scalar_one_or_none()
    
    if not user:
        # Yeni Kullanıcı
        user = User(
            telegram_id=auth_data.telegram_id,
            username=auth_data.username,
            first_name=auth_data.first_name
        )
        db.add(user)
    else:
        # Mevcut Kullanıcı Güncelleme
        user.username = auth_data.username
        user.first_name = auth_data.first_name
        
    await db.commit()
    return {"message": "Success", "user_id": user.id, "telegram_id": user.telegram_id}

@router.get("/{user_id}/favorites")
async def get_user_favorites(user_id: int, db: AsyncSession = Depends(get_db)):
    """Kullanıcının favoriye aldığı oyuncuları listeler."""
    stmt = select(UserFavorite).options(
        selectinload(UserFavorite.player).selectinload(Player.team)
    ).where(UserFavorite.user_id == user_id)
    
    result = await db.execute(stmt)
    favorites = result.scalars().all()
    
    # Sadece player objelerini döndür
    return [fav.player for fav in favorites]

@router.post("/{user_id}/favorites/{player_id}")
async def toggle_favorite(user_id: int, player_id: int, db: AsyncSession = Depends(get_db)):
    """Oyuncuyu favorilere ekler veya çıkarır (Toggle)."""
    # Önce kullanıcının mevcut favorisi mi kontrol et
    stmt = select(UserFavorite).where(
        UserFavorite.user_id == user_id,
        UserFavorite.player_id == player_id
    )
    favorite = (await db.execute(stmt)).scalar_one_or_none()
    
    if favorite:
        # Favori varsa Sil
        await db.delete(favorite)
        await db.commit()
        return {"message": "Oyuncu favorilerden çıkarıldı.", "action": "removed"}
    else:
        # Favori yoksa Ekle
        new_fav = UserFavorite(user_id=user_id, player_id=player_id)
        db.add(new_fav)
        await db.commit()
        return {"message": "Oyuncu favorilere eklendi.", "action": "added"}
