from fastapi import APIRouter

router = APIRouter(prefix="/api/bestiary", tags=["Bestiary"])

@router.get("/status")
def status():
    return {"modulo": "Bestiary", "status": "ok"}
