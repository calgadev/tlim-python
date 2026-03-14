from models.creature import Creature
from models.bestiary import BestiaryEntry

CHARMS = {
    "Wound":    300,
    "Enflame":  300,
    "Poison":   300,
    "Freeze":   300,
    "Zap":      300,
    "Curse":    300,
    "Cripple":  500,
    "Parry":    500,
    "Dodge":    500,
    "Adrenaline Burst": 500,
    "Numb":     500,
    "Cleanse":  500,
    "Bless":    2000,
    "Scavenge": 2000,
    "Gut":      2000,
    "Low Blow": 2000,
    "Divine":   2000,
    "Void":     2000,
}

def get_charm_cost(charm_name: str) -> int | None:
    return CHARMS.get(charm_name)

def calcular_sugestoes_charm(
    charm_desejado: str,
    db,
    user_id: int = 1
) -> dict:
    custo = get_charm_cost(charm_desejado)
    if custo is None:
        return {"erro": f"Charm '{charm_desejado}' não encontrado"}

    # Calcular pontos atuais
    entradas_completas = db.query(BestiaryEntry).filter(
        BestiaryEntry.user_id == user_id,
        BestiaryEntry.completed == True
    ).all()

    pontos_atuais = 0
    for entrada in entradas_completas:
        criatura = db.query(Creature).filter(
            Creature.id == entrada.creature_id
        ).first()
        if criatura:
            pontos_atuais += criatura.charm_points

    pontos_faltando = max(0, custo - pontos_atuais)

    # Buscar criaturas não completadas ordenadas por kills restantes
    entradas_incompletas = db.query(BestiaryEntry).filter(
        BestiaryEntry.user_id == user_id,
        BestiaryEntry.completed == False
    ).all()

    ids_em_progresso = {e.creature_id for e in entradas_incompletas}

    sugestoes = []

    # Criaturas já iniciadas
    for entrada in entradas_incompletas:
        criatura = db.query(Creature).filter(
            Creature.id == entrada.creature_id
        ).first()
        if not criatura:
            continue
        kills_restantes = criatura.kills_required - entrada.kills_current
        sugestoes.append({
            "creature": criatura.name,
            "kills_remaining": kills_restantes,
            "charm_points": criatura.charm_points,
            "status": "em progresso"
        })

    # Criaturas ainda não iniciadas
    todas_criaturas = db.query(Creature).all()
    for criatura in todas_criaturas:
        if criatura.id not in ids_em_progresso:
            sugestoes.append({
                "creature": criatura.name,
                "kills_remaining": criatura.kills_required,
                "charm_points": criatura.charm_points,
                "status": "não iniciado"
            })

    # Ordenar por kills restantes (menos kills = mais fácil de completar)
    sugestoes.sort(key=lambda x: (x["kills_remaining"], -x["charm_points"]))

    return {
        "charm": charm_desejado,
        "custo_total": custo,
        "pontos_atuais": pontos_atuais,
        "pontos_faltando": pontos_faltando,
        "pode_comprar": pontos_atuais >= custo,
        "sugestoes": sugestoes[:10]
    }


def listar_charms() -> list[dict]:
    return [{"name": k, "cost": v} for k, v in sorted(CHARMS.items(), key=lambda x: x[1])]