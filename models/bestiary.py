from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base

class BestiaryEntry(Base):
    __tablename__ = "bestiary_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    creature_id = Column(Integer, ForeignKey("creatures.id"), nullable=False)
    kills_current = Column(Integer, nullable=False, default=0)
    completed = Column(Boolean, default=False)

    creature = relationship("Creature")