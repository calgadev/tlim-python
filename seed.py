import json
from models.database import SessionLocal, engine, Base
from models import item, creature, inventory, bestiary
from models.item import Item
from models.creature import Creature

Base.metadata.create_all(bind=engine)

def seed_items(db):
    total = db.query(Item).count()
    if total > 0:
        print(f"Itens já cadastrados ({total} registros). Pulando...")
        return

    with open("seed_data/items.json", "r", encoding="utf-8") as f:
        items = json.load(f)

    for i in items:
        db.add(Item(
            name=i["name"],
            weight=i["weight"],
            npc_price=i["npc_price"],
            npc_seller=i.get("npc_seller"),
            is_imbuement_material=i["is_imbuement_material"],
            imbuement_name=i.get("imbuement_name")
        ))

    db.commit()
    print(f"{len(items)} itens inseridos com sucesso.")

def seed_creatures(db):
    total = db.query(Creature).count()
    if total > 0:
        print(f"Criaturas já cadastradas ({total} registros). Pulando...")
        return

    with open("seed_data/creatures.json", "r", encoding="utf-8") as f:
        creatures = json.load(f)

    for c in creatures:
        db.add(Creature(
            name=c["name"],
            kills_required=c["kills_required"],
            charm_points=c["charm_points"]
        ))

    db.commit()
    print(f"{len(creatures)} criaturas inseridas com sucesso.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Iniciando seed do banco de dados...")
        seed_items(db)
        seed_creatures(db)
        print("Seed concluído.")
    finally:
        db.close()