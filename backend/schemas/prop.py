from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from schemas.player import PlayerSearchResponse, GameBase

class PropLineBase(BaseModel):
    id: int
    market: str
    line: float
    over_odds: Optional[int] = None
    under_odds: Optional[int] = None
    bookmaker: str
    
    model_config = ConfigDict(from_attributes=True)

class PropLineResponse(PropLineBase):
    player: PlayerSearchResponse
    game: GameBase
    
    model_config = ConfigDict(from_attributes=True)

class HitRateHistory(BaseModel):
    game_id: int
    value: float
    line: float
    is_hit: bool

class HitRateStat(BaseModel):
    hit_rate: float
    hits: int
    total: int
    history: List[HitRateHistory]

class PropAnalyticsResponse(BaseModel):
    prop_id: int
    market: str
    line: float
    hit_rates: Dict[str, HitRateStat] # l5, l10, l20, season
    matchup_grade: Dict[str, Any]
    prediction: Dict[str, Any]
    splits: Dict[str, float]
