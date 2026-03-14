from schemas.hunt_schema import HuntImportSchema, ItemColetado, CreaturaAbatida

def parse_json_hunt(data: dict) -> HuntImportSchema:
    items = []
    for item in data.get("items", []):
        items.append(ItemColetado(
            name=item["name"],
            quantity=item["quantity"]
        ))

    creatures = []
    for creature in data.get("creatures", []):
        creatures.append(CreaturaAbatida(
            name=creature["name"],
            kills=creature["kills"]
        ))

    return HuntImportSchema(
        duration_minutes=data.get("duration_minutes"),
        raw_profit=data.get("raw_profit"),
        items=items,
        creatures=creatures
    )