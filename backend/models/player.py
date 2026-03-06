from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    balldontlie_id = Column(Integer, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    position = Column(String(10))
    jersey_number = Column(String(10))
    headshot_url = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStat", back_populates="player")
    prop_lines = relationship("PropLine", back_populates="player")
    favorited_by = relationship("UserFavorite", back_populates="player")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
