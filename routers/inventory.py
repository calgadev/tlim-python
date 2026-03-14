from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.item import Item
from models.inventory import UserInventory

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

USER_ID = 1

@router.get("/")
def listar_inventario(db: Session = Depends(get_db)):
    entradas = db.query(UserInventory).filter(
        UserInventory.user_id == USER_ID
    ).all()

    resultado = []
    total_value = 0

    for entrada in entradas:
        item = db.query(Item).filter(Item.id == entrada.item_id).first()
        if not item:
            continue

        estimated_value = item.npc_price * entrada.quantity
        total_value += estimated_value

        resultado.append({
            "item": item.name,
            "quantity": entrada.quantity,
            "goal_quantity": entrada.goal_quantity,
            "goal_reached": entrada.quantity >= entrada.goal_quantity if entrada.goal_quantity > 0 else None,
            "npc_price": item.npc_price,
            "npc_seller": item.npc_seller,
            "is_imbuement_material": item.is_imbuement_material,
            "imbuement_name": item.imbuement_name,
            "estimated_value": estimated_value
        })

    resultado.sort(key=lambda x: x["estimated_value"], reverse=True)

    return {
        "total_items": len(resultado),
        "total_estimated_value": total_value,
        "items": resultado
    }

@router.put("/goal")
def definir_meta(payload: dict, db: Session = Depends(get_db)):
    item_name = payload.get("item_name")
    goal_quantity = payload.get("goal_quantity")

    if not item_name or goal_quantity is None:
        raise HTTPException(status_code=400, detail="item_name e goal_quantity são obrigatórios")

    item = db.query(Item).filter(Item.name.ilike(item_name)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    inventario = db.query(UserInventory).filter(
        UserInventory.user_id == USER_ID,
        UserInventory.item_id == item.id
    ).first()

    if inventario:
        inventario.goal_quantity = goal_quantity
    else:
        db.add(UserInventory(
            user_id=USER_ID,
            item_id=item.id,
            quantity=0,
            goal_quantity=goal_quantity
        ))

    db.commit()
    return {"mensagem": f"Meta de {goal_quantity}x {item.name} definida com sucesso"}