from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import SavedPick, PropLine, Player, Game

router = APIRouter()

@router.get("/best")
async def get_best_picks(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """AI tarafından önerilen, Edge (EV) ve Hit olasılığı yüksek seçimler."""
    # Gerçek sistemde arkaplanda pre-calculate edilip cachelenmeli ama demonstrasyon için boş liste
    # İleride cache'den okunacak: redis_client.get('best_picks_today')
    return []

@router.post("/save")
async def save_user_pick(prop_id: int, pick_type: str, user_id: int, notes: str = None, db: AsyncSession = Depends(get_db)):
    """Kullanıcının tercih ettiği prop bahsini kaydeder (Takip için)."""
    if pick_type not in ["Over", "Under"]:
        raise HTTPException(status_code=400, detail="Invalid pick type. Must be 'Over' or 'Under'")
        
    saved_pick = SavedPick(user_id=user_id, prop_line_id=prop_id, pick_type=pick_type, notes=notes)
    db.add(saved_pick)
    await db.commit()
    
    return {"message": "Kullanıcı seçimi kaydedildi", "pick_id": saved_pick.id}

@router.get("/user/{telegram_id}")
async def get_user_picks(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Kullanıcının geçmiş kayıtlı seçimlerini ve sonuçlarını gösterir."""
    from models.user import User
    
    # Telegram ID den user ID bul
    user = (await db.execute(select(User).where(User.telegram_id == telegram_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        
    stmt = select(SavedPick).options(
        selectinload(SavedPick.prop_line).selectinload(PropLine.player).selectinload(Player.team),
        selectinload(SavedPick.prop_line).selectinload(PropLine.game)
    ).where(SavedPick.user_id == user.id).order_by(SavedPick.created_at.desc())
    
    result = await db.execute(stmt)
    return result.scalars().all()
