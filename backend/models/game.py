from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    balldontlie_id = Column(Integer, unique=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    home_team_score = Column(Integer, default=0)
    away_team_score = Column(Integer, default=0)
    status = Column(String, default="Scheduled") # Scheduled, In Progress, Final
    season = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")
    player_stats = relationship("PlayerStat", back_populates="game")
    prop_lines = relationship("PropLine", back_populates="game")
