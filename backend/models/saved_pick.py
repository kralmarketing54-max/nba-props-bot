from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class SavedPick(Base):
    __tablename__ = "saved_picks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    prop_line_id = Column(Integer, ForeignKey("prop_lines.id"), nullable=False)
    
    # User's pick: "Over" or "Under"
    pick_type = Column(String(10), nullable=False)
    
    # Optional notes from the user
    notes = Column(Text, nullable=True)
    
    # "Pending", "Won", "Lost" (Can be updated automatically after the game)
    status = Column(String(20), default="Pending")
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="saved_picks")
    prop_line = relationship("PropLine", back_populates="saved_picks")
