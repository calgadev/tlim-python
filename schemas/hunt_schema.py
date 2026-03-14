from pydantic import BaseModel
from typing import Optional

class ItemColetado(BaseModel):
    name: str
    quantity: int

class CreaturaAbatida(BaseModel):
    name: str
    kills: int

class HuntImportSchema(BaseModel):
    duration_minutes: Optional[int] = None
    raw_profit: Optional[int] = None
    items: list[ItemColetado] = []
    creatures: list[CreaturaAbatida] = []