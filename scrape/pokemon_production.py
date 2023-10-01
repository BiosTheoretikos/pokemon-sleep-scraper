import csv
import json
from typing import NamedTuple

import requests

with open("export/game-en.json", "r", encoding="utf-8") as f_game:
    game_data = json.load(f_game)

POKEMON_NAME_TO_ID = {
    name: int(pokemon_id)
    for pokemon_id, name in game_data["PokemonName"].items()
}

CONFIDENCE_TO_ID = {
    "Very good": 2,
    "Good": 1,
    "Decent": 0,
    "Poor": -1,
    "Very poor": -2,
}

default_split = 0.2

with open("data/pokemon_data.json") as f:
    pokemon_data = json.load(f)


def download_gsheet_csv(file_id, sheet_id):
    r = requests.get(f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&id={file_id}&gid={sheet_id}")
    return r.content.decode("utf-8")


def is_info_header(row):
    return tuple(row[:6]) == ("Pokemon", "Ingr%", "Confidence", "skill% * skill value", "Confidence", "# of entries")


def is_empty_row(row):
    return all(not data for data in row)


def is_incomplete_info_row(row):
    return any(not data for data in row[:6])


def get_production_data(row=None):
    if not row or is_incomplete_info_row(row):
        return {
            "dataCount": 0,
            "ingredientSplit": default_split,
            "skillValue": 0,
            "confidence": {
                "ingredient": CONFIDENCE_TO_ID["Very poor"],
                "skill": CONFIDENCE_TO_ID["Very poor"],
            }
        }

    return {
        "dataCount": int(row.data_count),
        "ingredientSplit": float(row.ingredient_split.replace("%", "")) / 100,
        "skillValue": float(row.skill_value),
        "confidence": {
            "ingredient": CONFIDENCE_TO_ID[row.ingredient_split_confidence],
            "skill": CONFIDENCE_TO_ID[row.skill_value_confidence],
        }
    }


class RpModelInfoRow(NamedTuple):
    pokemon_name: str
    ingredient_split: str
    ingredient_split_confidence: str
    skill_value: str
    skill_value_confidence: str
    data_count: str


def get_rp_model_data():
    data_by_pokemon = {}

    file_id = "1kBrPl0pdAO8gjOf_NrTgAPseFtqQA27fdfEbMBBeAhs"
    sheet_id = "1673887151"

    csv_content = download_gsheet_csv(file_id, sheet_id)
    sheet_reader = csv.reader(csv_content.splitlines(), delimiter=",")

    found_info_header = False
    for row in sheet_reader:
        if not found_info_header:
            if not is_info_header(row):
                continue

            found_info_header = True
            continue

        if is_empty_row(row):
            break

        row = RpModelInfoRow(*row[:6])

        data_by_pokemon[POKEMON_NAME_TO_ID[row.pokemon_name]] = get_production_data(row)

    return data_by_pokemon


def main():
    rp_model_data = get_rp_model_data()

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

    with open(f"export/pokemon_production.json", "w+", encoding="utf-8", newline="\n") as f_export:
        json.dump(data, f_export, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()