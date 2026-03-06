from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone, timedelta

from database import get_db
from models import PropLine, Player, Game, PlayerStat
from services.analytics import analytics_service
from services.matchup import matchup_service
from services.prediction import prediction_service
from schemas.prop import PropAnalyticsResponse

router = APIRouter()

@router.get("/today")
async def get_today_props(db: AsyncSession = Depends(get_db)):
    """Bugünün güncel prop bahislerini getirir."""
    # Sadece bugünden sonraki maçların (Upcoming) propları
    today = datetime.now(timezone.utc)
    
    stmt = select(PropLine).options(
        selectinload(PropLine.player).selectinload(Player.team),
        selectinload(PropLine.game)
    ).join(Game).where(Game.date >= today).limit(50)
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/player/{player_id}")
async def get_player_props(player_id: int, db: AsyncSession = Depends(get_db)):
    """Belirli bir oyuncunun aktif prop çizgilerini getirir."""
    today = datetime.now(timezone.utc)
    
    stmt = select(PropLine).options(
        selectinload(PropLine.game)
    ).join(Game).where(
        PropLine.player_id == player_id,
        Game.date >= today
    )
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{prop_id}/analytics")
async def get_prop_analytics(prop_id: int, db: AsyncSession = Depends(get_db)):
    """Belirli bir prop için hit rate, matchup grade ve AI tahminlerini getirir."""
    
    # 1. Prop'u bul
    stmt = select(PropLine).options(
        selectinload(PropLine.player),
        selectinload(PropLine.game)
    ).where(PropLine.id == prop_id)
    
    prop = (await db.execute(stmt)).scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Prop Line bulunamadı")

    # 2. Oyuncunun tüm istatistik geçmişini al (sondan başa tarihli)
    stat_stmt = select(PlayerStat).options(selectinload(PlayerStat.game)).join(Game).where(
        PlayerStat.player_id == prop.player_id
    ).order_by(Game.date.desc())
    stats = list((await db.execute(stat_stmt)).scalars().all())

    if not stats:
        raise HTTPException(status_code=404, detail="Oyuncuya ait geçmiş istatistik bulunamadı")

    # 3. Hit Rates
    hit_rates = analytics_service.get_comprehensive_hit_rates(stats=stats, market=prop.market, line=prop.line)
    
    # 4. Splits (Home/Away, H2H)  - (Not: prop.game'den rakibi buluruz)
    is_home = (prop.game.home_team_id == prop.player.team_id)
    opponent_id = prop.game.away_team_id if is_home else prop.game.home_team_id
    splits = analytics_service.calculate_splits(stats=stats, current_team_id=prop.player.team_id, opponent_team_id=opponent_id, market=prop.market)
    
    # 5. Prediction (EV, Hit Prob)
    prediction = prediction_service.calculate_prediction(
        stats=stats[:20], # Son 20 maça göre tahmin yapsın
        market=prop.market, 
        line=prop.line, 
        over_odds=prop.over_odds
    )
    
    # 6. Matchup Grade
    matchup_grade = matchup_service.calculate_matchup_grade(
        player_avg_stats=prediction["mean"],
        vegas_line=prop.line,
        l5_hit_rate=hit_rates["l5"]["hit_rate"],
        opponent_defensive_rating=15, # FIXME: Rakip takım rankını statik verdik, ileride DB table'a bağlanacak
        head_to_head_avg=splits["h2h_avg"]
    )

    return {
        "prop_id": prop.id,
        "market": prop.market,
        "line": prop.line,
        "hit_rates": hit_rates,
        "matchup_grade": matchup_grade,
        "prediction": prediction,
        "splits": splits
    }
