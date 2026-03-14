import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.item import Item
from models.creature import Creature
from models.inventory import UserInventory
from models.bestiary import BestiaryEntry
from parsers.json_hunt_parser import parse_json_hunt
from parsers.text_hunt_parser import parse_text_hunt
from schemas.hunt_schema import HuntImportSchema

router = APIRouter(prefix="/api/hunt", tags=["Hunt"])

USER_ID = 1

def processar_hunt(hunt: HuntImportSchema, db: Session):
    # Atualizar inventário
    for item_coletado in hunt.items:
        item_db = db.query(Item).filter(
            Item.name.ilike(item_coletado.name)
        ).first()
        if not item_db:
            continue

        inventario = db.query(UserInventory).filter(
            UserInventory.user_id == USER_ID,
            UserInventory.item_id == item_db.id
        ).first()

        if inventario:
            inventario.quantity += item_coletado.quantity
        else:
            db.add(UserInventory(
                user_id=USER_ID,
                item_id=item_db.id,
                quantity=item_coletado.quantity,
                goal_quantity=0
            ))

    # Atualizar bestiário
    for criatura_abatida in hunt.creatures:
        criatura_db = db.query(Creature).filter(
            Creature.name.ilike(criatura_abatida.name)
        ).first()
        if not criatura_db:
            continue

        entrada = db.query(BestiaryEntry).filter(
            BestiaryEntry.user_id == USER_ID,
            BestiaryEntry.creature_id == criatura_db.id
        ).first()

        if entrada:
            entrada.kills_current += criatura_abatida.kills
            if entrada.kills_current >= criatura_db.kills_required:
                entrada.completed = True
        else:
            kills = criatura_abatida.kills
            db.add(BestiaryEntry(
                user_id=USER_ID,
                creature_id=criatura_db.id,
                kills_current=kills,
                completed=kills >= criatura_db.kills_required
            ))

    db.commit()
    return {"mensagem": "Hunt processada com sucesso"}

@router.post("/import/json")
async def importar_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser .json")

    conteudo = await file.read()
    try:
        data = json.loads(conteudo)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    hunt = parse_json_hunt(data)
    return processar_hunt(hunt, db)

@router.post("/import/text")
async def importar_texto(payload: dict, db: Session = Depends(get_db)):
    texto = payload.get("text", "")
    if not texto:
        raise HTTPException(status_code=400, detail="Texto não pode ser vazio")

    hunt = parse_text_hunt(texto)
    return processar_hunt(hunt, db)