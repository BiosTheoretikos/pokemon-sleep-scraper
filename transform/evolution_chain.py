import json

from _const import *

DATA_FILE_PATH = "unprocessed/pokemon_evo_chain.json"

with open(DATA_FILE_PATH, "r", encoding="utf-8") as f_game:
    evo_chain_data = json.load(f_game)

with open("transformed/game-en.json", "r", encoding="utf-8") as f_game:
    game_data = json.load(f_game)

ITEM_NAME_TO_ID = {
    name.replace("“", "").replace("”", "").replace("’", "'"): int(item_id)
    for item_id, name in game_data["Item"].items()
}

ID_EEVEE = 133
ID_SLOWPOKE = 79


def transform_evolution_condition(evolution):
    conditions = []
    for condition in evolution["conditions"]:
        if condition.startswith("Level"):
            conditions.append({
                "type": "level",
                "level": int(condition.split(" ")[1])
            })
            continue

        if condition.endswith("Candy"):
            conditions.append({
                "type": "candy",
                "count": int(condition.split(" ")[0])
            })
            continue

        if condition.startswith("Sleep for"):
            conditions.append({
                "type": "sleepTime",
                "hours": int(condition.split(" ")[2])
            })
            continue

        if condition.startswith("Evolve between"):
            _, _, start, _, end = condition.split(" ")

            timing_dict = {
                "6am": 6,
                "6pm": 18
            }

            conditions.append({
                "type": "timing",
                "startHour": timing_dict[start],
                "endHour": timing_dict[end],
            })
            continue

        if condition.startswith("Use the"):
            txt = condition.split(" ", 2)[2]
            conditions.append({
                "type": "item",
                "item": ITEM_NAME_TO_ID[txt]
            })

    return {
        "id": int(evolution["id"]),
        "conditions": conditions
    }


def main():
    evo_chain_list = [
        {
            "pokemon": pokemon_id,
            "next": [],
            "stage": 1,
            "previous": None
        }
        for pokemon_id in POKEMON_WITHOUT_EVO_CHAIN
    ]

    for initial_id, evolutions in evo_chain_data.items():
        initial_id = int(initial_id)

        initial = {
            "pokemon": initial_id,
            "next": [],
            "stage": 1,
            "previous": None
        }

        if initial_id in (ID_EEVEE, ID_SLOWPOKE):
            for evolution in evolutions:
                current = {
                    "pokemon": int(evolution["id"]),
                    "next": [],
                    "stage": initial["stage"] + 1,
                    "previous": initial["pokemon"]
                }
                initial["next"].append(transform_evolution_condition(evolution))
                evo_chain_list.append(current)
        else:
            for evolution in evolutions:
                initial["next"].append(transform_evolution_condition(evolution))
                current = {
                    "pokemon": int(evolution["id"]),
                    "next": [],
                    "stage": initial["stage"] + 1,
                    "previous": initial["pokemon"]
                }
                evo_chain_list.append(initial)
                initial = current

        evo_chain_list.append(initial)

    with open(f"transformed/evolution_chain.json", "w+", encoding="utf-8", newline="\n") as f:
        json.dump(evo_chain_list, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
