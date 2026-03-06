from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class PropLine(Base):
    __tablename__ = "prop_lines"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)
    
    # e.g., 'player_points', 'player_rebounds', 'player_assists', 'player_threes', 'player_points_rebounds_assists'
    market = Column(String(50), nullable=False, index=True)
    line = Column(Float, nullable=False)
    over_odds = Column(Integer)  # American odds format (-110, +120 vs)
    under_odds = Column(Integer)
    bookmaker = Column(String(50), default="DraftKings")
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    player = relationship("Player", back_populates="prop_lines")
    game = relationship("Game", back_populates="prop_lines")
    saved_picks = relationship("SavedPick", back_populates="prop_line")
