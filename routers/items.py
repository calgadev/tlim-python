from fastapi import APIRouter

router = APIRouter(prefix="/api/items", tags=["Items"])

@router.get("/status")
def status():
    return {"modulo": "Items", "status": "ok"}
