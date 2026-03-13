from fastapi import APIRouter

router = APIRouter(prefix="/api/hunt", tags=["Hunt"])

@router.get("/status")
def status():
    return {"modulo": "Hunt", "status": "ok"}
