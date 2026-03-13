from sqlalchemy import Column, Integer, String
from models.database import Base

class Creature(Base):
    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    kills_required = Column(Integer, nullable=False)
    charm_points = Column(Integer, nullable=False, default=0)