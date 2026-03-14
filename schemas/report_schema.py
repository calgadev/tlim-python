from pydantic import BaseModel
from typing import Optional

class ItemDecisao(BaseModel):
    name: str
    quantity: int
    decision: str
    sell_to: Optional[str] = None
    reason: str
    estimated_value: int

class BestiarioUpdate(BaseModel):
    creature: str
    kills_before: int
    kills_after: int
    total_required: int
    completed: bool
    charm_points_earned: Optional[int] = None

class HuntReportSchema(BaseModel):
    session_id: int
    duration_minutes: Optional[int] = None
    raw_profit: Optional[int] = None
    items: list[ItemDecisao] = []
    bestiary_updates: list[BestiarioUpdate] = []