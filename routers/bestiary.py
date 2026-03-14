from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from services.bestiary_service import get_progresso_bestiary, get_total_charm_points
from services.charm_calculator_service import calcular_sugestoes_charm, listar_charms

router = APIRouter(prefix="/api/bestiary", tags=["Bestiary"])

USER_ID = 1

@router.get("/")
def listar_progresso(db: Session = Depends(get_db)):
    progresso = get_progresso_bestiary(db, USER_ID)
    total_pontos = get_total_charm_points(db, USER_ID)
    return {
        "total_charm_points": total_pontos,
        "total_creatures": len(progresso),
        "completed": sum(1 for c in progresso if c["completed"]),
        "in_progress": sum(1 for c in progresso if not c["completed"]),
        "creatures": progresso
    }

@router.get("/charms")
def listar_charms_disponiveis():
    return listar_charms()

@router.get("/charms/{charm_name}")
def sugerir_criaturas_para_charm(
    charm_name: str,
    db: Session = Depends(get_db)
):
    resultado = calcular_sugestoes_charm(charm_name, db, USER_ID)
    if "erro" in resultado:
        raise HTTPException(status_code=404, detail=resultado["erro"])
    return resultado