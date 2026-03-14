from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.item import Item
from models.creature import Creature

router = APIRouter(prefix="/api/items", tags=["Items"])

router = APIRouter(prefix="/api/items", tags=["Items"])

@router.get("/")
def listar_itens(db: Session = Depends(get_db)):
    itens = db.query(Item).all()
    return itens

@router.get("/{item_id}")
def buscar_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return {"erro": "Item não encontrado"}
    return item

@router.get("/creatures/")
def listar_criaturas(db: Session = Depends(get_db)):
    criaturas = db.query(Creature).all()
    return criaturas

@router.get("/creatures/{creature_id}")
def buscar_criatura(creature_id: int, db: Session = Depends(get_db)):
    criatura = db.query(Creature).filter(Creature.id == creature_id).first()
    if not criatura:
        return {"erro": "Criatura não encontrada"}
    return criatura