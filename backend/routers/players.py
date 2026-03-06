from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload
from typing import List

from database import get_db
from models import Player, PlayerStat
from schemas.player import PlayerSearchResponse, PlayerBase

router = APIRouter()

@router.get("/search", response_model=List[PlayerSearchResponse])
async def search_players(q: str = Query(..., min_length=2), limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Oyuncu arama (autocomplete). İsim veya soyisme göre arar."""
    
    # İsim veya soyisimde '%q%' arar (Büyük/küçük harf duyarsız - ilike)
    stmt = select(Player).options(selectinload(Player.team)).where(
        or_(
            Player.first_name.ilike(f"%{q}%"),
            Player.last_name.ilike(f"%{q}%")
        )
    ).limit(limit)
    
    result = await db.execute(stmt)
    players = result.scalars().all()
    
    return players

@router.get("/{player_id}")
async def get_player_details(player_id: int, db: AsyncSession = Depends(get_db)):
    """Belirli bir oyuncunun profil bilgilerini (takımıyla birlikte) getirir."""
    stmt = select(Player).options(selectinload(Player.team)).where(Player.id == player_id)
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()
    
    if not player:
        raise HTTPException(status_code=404, detail="Oyuncu bulunamadı")
        
    return player

@router.get("/{player_id}/stats")
async def get_player_stats(player_id: int, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Oyuncunun son N maçlık istatistiklerini getirir."""
    from models.game import Game
    
    stmt = select(PlayerStat).options(selectinload(PlayerStat.game)).join(Game).where(
        PlayerStat.player_id == player_id
    ).order_by(Game.date.desc()).limit(limit)
    
    result = await db.execute(stmt)
    stats = result.scalars().all()
    
    return stats
