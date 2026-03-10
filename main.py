from fastapi import FastAPI

app = FastAPI(title="TLIM - Tibia Loot & Inventory Manager")

@app.get("/")
def inicio():
    return {"mensagem": "TLIM está no ar!"}