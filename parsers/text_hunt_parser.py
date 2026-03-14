import re
from schemas.hunt_schema import HuntImportSchema, ItemColetado, CreaturaAbatida

def parse_text_hunt(text: str) -> HuntImportSchema:
    items_dict = {}
    creatures_dict = {}

    loot_pattern = re.compile(
        r"Loot of (?:a |an )?(.+?):\s*(.+)"
    )
    item_pattern = re.compile(
        r"(\d+)?\s*(?:a |an )?([a-zA-Z][a-zA-Z\s]+)"
    )

    for line in text.strip().split("\n"):
        match = loot_pattern.match(line.strip())
        if not match:
            continue

        creature_name = match.group(1).strip()
        loot_string = match.group(2).strip()

        creatures_dict[creature_name] = creatures_dict.get(creature_name, 0) + 1

        for loot_item in loot_string.split(","):
            loot_item = loot_item.strip()
            item_match = item_pattern.match(loot_item)
            if not item_match:
                continue

            quantity = int(item_match.group(1)) if item_match.group(1) else 1
            item_name = item_match.group(2).strip().rstrip("s") \
                if item_match.group(1) else item_match.group(2).strip()

            if item_name.lower() in ["nothing", "gold coin", ""]:
                continue

            if item_name in items_dict:
                items_dict[item_name] += quantity
            else:
                items_dict[item_name] = quantity

    items = [ItemColetado(name=k, quantity=v) for k, v in items_dict.items()]
    creatures = [CreaturaAbatida(name=k, kills=v) for k, v in creatures_dict.items()]

    return HuntImportSchema(items=items, creatures=creatures)