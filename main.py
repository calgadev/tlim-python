from fastapi import FastAPI
from models.database import engine, Base
from models import item, creature, inventory, bestiary
from routers import hunt, bestiary as bestiary_router, inventory as inventory_router, items

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TLIM - Tibia Loot & Inventory Manager",
    description="Gerencie seu loot e bestiário do Tibia",
    version="1.0.0"
)

app.include_router(hunt.router)
app.include_router(bestiary_router.router)
app.include_router(inventory_router.router)
app.include_router(items.router)

@app.get("/")
def inicio():
    return {"mensagem": "TLIM está no ar!"}