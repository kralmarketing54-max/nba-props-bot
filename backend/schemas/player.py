from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class TeamBase(BaseModel):
    id: int
    name: str
    abbreviation: str
    conference: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class PlayerBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: Optional[str] = None
    jersey_number: Optional[str] = None
    headshot_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class PlayerSearchResponse(PlayerBase):
    team: TeamBase
    full_name: str
    
    model_config = ConfigDict(from_attributes=True)

class PlayerStatsBase(BaseModel):
    id: int
    pts: int
    reb: int
    ast: int
    stl: int
    blk: int
    turnover: int
    fg3m: int
    min: str
    
    model_config = ConfigDict(from_attributes=True)

class GameBase(BaseModel):
    id: int
    date: datetime
    home_team_score: int
    away_team_score: int
    status: str
    
    model_config = ConfigDict(from_attributes=True)
    
class PlayerStatsWithGame(PlayerStatsBase):
    game: GameBase
    
    model_config = ConfigDict(from_attributes=True)
