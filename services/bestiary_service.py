from models.creature import Creature
from models.bestiary import BestiaryEntry
from schemas.report_schema import BestiarioUpdate

def get_progresso_bestiary(db, user_id: int = 1) -> list[dict]:
    entradas = db.query(BestiaryEntry).filter(
        BestiaryEntry.user_id == user_id
    ).all()

    resultado = []
    for entrada in entradas:
        criatura = db.query(Creature).filter(
            Creature.id == entrada.creature_id
        ).first()
        if not criatura:
            continue

        percentual = round(
            (entrada.kills_current / criatura.kills_required) * 100, 1
        )

        resultado.append({
            "creature": criatura.name,
            "kills_current": entrada.kills_current,
            "kills_required": criatura.kills_required,
            "kills_remaining": max(0, criatura.kills_required - entrada.kills_current),
            "progress_percent": min(100.0, percentual),
            "completed": entrada.completed,
            "charm_points": criatura.charm_points if entrada.completed else 0
        })

    resultado.sort(key=lambda x: (x["completed"], -x["progress_percent"]))
    return resultado


def get_total_charm_points(db, user_id: int = 1) -> int:
    entradas = db.query(BestiaryEntry).filter(
        BestiaryEntry.user_id == user_id,
        BestiaryEntry.completed == True
    ).all()

    total = 0
    for entrada in entradas:
        criatura = db.query(Creature).filter(
            Creature.id == entrada.creature_id
        ).first()
        if criatura:
            total += criatura.charm_points
    return total