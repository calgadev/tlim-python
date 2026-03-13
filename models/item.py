from sqlalchemy import Column, Integer, String, Float, Boolean
from models.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    weight = Column(Float, nullable=False, default=0.0)
    npc_price = Column(Integer, nullable=False, default=0)
    npc_seller = Column(String, nullable=True)
    is_imbuement_material = Column(Boolean, default=False)
    imbuement_name = Column(String, nullable=True)