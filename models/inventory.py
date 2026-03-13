from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base

class UserInventory(Base):
    __tablename__ = "user_inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    goal_quantity = Column(Integer, nullable=False, default=0)

    item = relationship("Item")