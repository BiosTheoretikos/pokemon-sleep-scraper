import csv
import json
import time
from typing import NamedTuple

import requests

from calc.entry import get_rp_model_df

with open("data/transformed/game-en.json", "r", encoding="utf-8") as f_game:
    game_data = json.load(f_game)

with open("data/scraped/pokemon_data.json", "r", encoding="utf-8") as f_pokemon:
    pokemon_data = json.load(f_pokemon)

POKEMON_NAME_TO_ID = {
    name: int(pokemon_id)
    for pokemon_id, name in game_data["PokemonName"].items()
}

POKEMON_ID_TO_MAIN_SKILL_ID = {
    data["id"]: data["skill"]
    for data in pokemon_data
}

SKILL_VALUE_IN_RP = {
    1: 400,  # Charge Strength S (#)
    2: 880,  # Charge Strength M
    3: 0,  # Dream Shard Magnet S (#)
    4: 0,  # Energizing Cheer S
    5: 0,  # Charge Strength S (#1 ~ #2)
    6: 0,  # Dream Shard Magnet S (#1 ~ #2)
    7: 0,  # Charge Energy S
    8: 0,  # Energy for Everyone S
    9: 0,  # Extra Helpful S
    10: 800,  # Ingredient Magnet S
    11: 0,  # Cooking Power-Up S
    12: 0,  # Type Boost S
    13: 0,  # Metronome
}

DEFAULT_SPLIT = 0.2

DEFAULT_PRODUCTION_DATA = {
    "dataCount": 0,
    "ingredientSplit": DEFAULT_SPLIT,
    "skillValue": 0,
    "error": {
        "ingredient": None,
        "skill": None,
    }
}

DIGIT_PRECISION = 8

with open("data/scraped/pokemon_data.json") as f:
    pokemon_data = json.load(f)


def get_main_skill_trigger_pct_dict(data):
    ret = {}

    for entry in data:
        pokemon_id = entry["pokemonId"]
        main_skill_id = POKEMON_ID_TO_MAIN_SKILL_ID[pokemon_id]

        skill_value = entry["skillValue"]
        if not skill_value:
            continue

        skill_value_in_rp = SKILL_VALUE_IN_RP[main_skill_id]
        if not skill_value_in_rp:
            continue

        ret[pokemon_id] = skill_value / skill_value_in_rp * 100

    return ret


def main():
    rp_model_data = get_rp_model_df()

    data = []

    for pokemon in pokemon_data:
        pokemon_id = pokemon["id"]
        rp_model_info = rp_model_data.get(pokemon_id)

        if not rp_model_info:
            print(f"No RP model data for Pokemon #{pokemon_id} ({game_data['PokemonName'][str(pokemon_id)]})")

        data.append(
            (rp_model_info or get_production_data()) |
            {
                "pokemonId": pokemon_id,
            }
        )

    skill_pct_dict = get_main_skill_trigger_pct_dict(data)
    data = [
        entry | {"skillPercent": round_value(skill_pct_dict.get(entry["pokemonId"]))}
        for entry in data
    ]

    with open(f"data/transformed/pokemon_production.json", "w+", encoding="utf-8", newline="\n") as f_export:
        json.dump(
            {
                "data": data,
                "lastUpdated": time.time(),
            },
            f_export,
            indent=2,
            ensure_ascii=False
        )


if __name__ == "__main__":
    main()
