from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    balldontlie_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String(10), nullable=False)
    conference = Column(String(50))
    division = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    players = relationship("Player", back_populates="team")
    home_games = relationship("Game", foreign_keys="[Game.home_team_id]", back_populates="home_team")
    away_games = relationship("Game", foreign_keys="[Game.away_team_id]", back_populates="away_team")
