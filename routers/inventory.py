from fastapi import APIRouter

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("/status")
def status():
    return {"modulo": "Inventory", "status": "ok"}
