from models.item import Item
from models.inventory import UserInventory
from schemas.report_schema import ItemDecisao

MARKET_PRICE_MULTIPLIER = 0.8

def decidir_destino_item(
    item_name: str,
    quantity: int,
    db,
    user_id: int = 1
) -> ItemDecisao | None:

    item_db = db.query(Item).filter(Item.name.ilike(item_name)).first()
    if not item_db:
        return None

    inventario = db.query(UserInventory).filter(
        UserInventory.user_id == user_id,
        UserInventory.item_id == item_db.id
    ).first()

    quantidade_atual = inventario.quantity if inventario else 0
    meta = inventario.goal_quantity if inventario else 0

    # Regra 1 — Meta de estoque não atingida
    if meta > 0 and quantidade_atual < meta:
        faltam = meta - quantidade_atual
        guardar = min(quantity, faltam)
        return ItemDecisao(
            name=item_db.name,
            quantity=quantity,
            decision="GUARDAR",
            sell_to=None,
            reason=f"Meta de estoque não atingida (atual: {quantidade_atual}, meta: {meta})",
            estimated_value=0
        )

    # Regra 2 — Material de Imbuement
    if item_db.is_imbuement_material:
        return ItemDecisao(
            name=item_db.name,
            quantity=quantity,
            decision="GUARDAR",
            sell_to=None,
            reason=f"Material de Imbuement: {item_db.imbuement_name}",
            estimated_value=0
        )

    # Regra 3 — Comparar NPC vs Market
    npc_price = item_db.npc_price
    market_price = int(npc_price * MARKET_PRICE_MULTIPLIER)

    if item_db.npc_seller and npc_price > 0:
        return ItemDecisao(
            name=item_db.name,
            quantity=quantity,
            decision="VENDER",
            sell_to=item_db.npc_seller,
            reason=f"NPC paga mais (NPC: {npc_price} gp, Market estimado: {market_price} gp)",
            estimated_value=npc_price * quantity
        )

    # Regra 4 — Sem NPC, vender no market
    if market_price > 0:
        return ItemDecisao(
            name=item_db.name,
            quantity=quantity,
            decision="VENDER NO MARKET",
            sell_to="Market",
            reason=f"Sem NPC comprador, vender no Market (estimado: {market_price} gp)",
            estimated_value=market_price * quantity
        )

    # Regra 5 — Sem valor conhecido
    return ItemDecisao(
        name=item_db.name,
        quantity=quantity,
        decision="VERIFICAR",
        sell_to=None,
        reason="Preço não cadastrado — verificar manualmente",
        estimated_value=0
    )


def gerar_relatorio_venda(items: list, db, user_id: int = 1) -> list[ItemDecisao]:
    relatorio = []
    for item in items:
        decisao = decidir_destino_item(item.name, item.quantity, db, user_id)
        if decisao:
            relatorio.append(decisao)
    return relatorio