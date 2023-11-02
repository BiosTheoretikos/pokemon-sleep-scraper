import csv
import json

from _const import *

DATA_FILE_PATH = "data_raw/ingredients.csv"

with open("data/transformed/game-en.json", "r", encoding="utf-8") as f_game:
    game_data = json.load(f_game)

POKEMON_NAME_TO_ID = {
    name: int(pokemon_id)
    for pokemon_id, name in game_data["PokemonName"].items()
}

with open("data/manual/pokemon/evolution_chain.json", "r", encoding="utf-8") as f_evo:
    chain_data = json.load(f_evo)

POKEMON_ID_TO_CHAIN_TAIL_ID = {
    pokemon_id: pokemon_id
    for pokemon_id in POKEMON_WITHOUT_EVO_CHAIN
}

for chain in chain_data:
    if not chain["next"]:
        POKEMON_ID_TO_CHAIN_TAIL_ID[chain["pokemon"]] = chain["pokemon"]
        continue

    next_chain_conditions = chain["next"]
    next_chain = next(chain for chain in chain_data if chain["pokemon"] == next_chain_conditions[0]["id"])
    while len(next_chain_conditions) == 1:
        next_chain = next(chain for chain in chain_data if chain["pokemon"] == next_chain_conditions[0]["id"])
        next_chain_conditions = next_chain["next"]

    if len(next_chain_conditions) > 1:
        print(f"1+ next, unable to decide for #{chain['pokemon']}")
        POKEMON_ID_TO_CHAIN_TAIL_ID[chain["pokemon"]] = chain["pokemon"]
    else:
        POKEMON_ID_TO_CHAIN_TAIL_ID[chain["pokemon"]] = next_chain["pokemon"]

# Force override for slowbro
POKEMON_ID_TO_CHAIN_TAIL_ID[79] = 80

INGREDIENT_NAME_TO_ID = {
    "leek": 1,
    "oil": 10,
    "ginger": 11,
    "tomato": 12,
    "cacao": 13,
    "tail": 14,
    "soybean": 15,
    "mushroom": 2,
    "egg": 3,
    "potato": 4,
    "apple": 5,
    "herb": 6,
    "sausage": 7,
    "milk": 8,
    "honey": 9,
}


def main():
    ingredient_of_chain = {}

    with open(DATA_FILE_PATH, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quotechar="|")
        for row in reader:
            pokemon_name = row[0]
            pokemon_id = POKEMON_NAME_TO_ID[pokemon_name]
            chain_origin_id = POKEMON_ID_TO_CHAIN_TAIL_ID[pokemon_id]

            ingredient_1_name = INGREDIENT_NAME_TO_ID[row[4].lower()]
            ingredient_1_qty = int(row[5])
            ingredient_30_1_id = INGREDIENT_NAME_TO_ID[row[6].lower()]
            ingredient_30_1_qty = int(row[7])
            ingredient_30_2_id = INGREDIENT_NAME_TO_ID[row[8].lower()]
            ingredient_30_2_qty = int(row[9])
            ingredient_60_1_id = INGREDIENT_NAME_TO_ID[row[12].lower()]
            ingredient_60_1_qty = int(row[13])
            ingredient_60_2_id = INGREDIENT_NAME_TO_ID[row[14].lower()]
            ingredient_60_2_qty = int(row[15])
            ingredient_60_3_id = INGREDIENT_NAME_TO_ID.get(row[16].lower(), None)
            ingredient_60_3_qty = int(row[17])

            lv_60 = [
                {"id": ingredient_60_1_id, "qty": ingredient_60_1_qty},
                {"id": ingredient_60_2_id, "qty": ingredient_60_2_qty},
            ]
            if ingredient_60_3_id:
                lv_60.append({"id": ingredient_60_3_id, "qty": ingredient_60_3_qty})

            print(f"Chain of #{chain_origin_id} ({pokemon_name})")
            ingredient_of_chain[chain_origin_id] = {
                "1": [
                    {"id": ingredient_1_name, "qty": ingredient_1_qty},
                ],
                "30": sorted([
                    {"id": ingredient_30_1_id, "qty": ingredient_30_1_qty},
                    {"id": ingredient_30_2_id, "qty": ingredient_30_2_qty}
                ], key=lambda item: item["id"]),
                "60": sorted(lv_60, key=lambda item: item["id"]),
            }

    with open(f"data/manual/pokemon/ingredient_chain.json", "w+", encoding="utf-8", newline="\n") as f:
        data = [
            {
                "chainId": origin_id,
                "ingredients": ingredient_chain
            }
            for origin_id, ingredient_chain in ingredient_of_chain.items()
        ]

        print(len(data))
        json.dump(data, f, indent=2, ensure_ascii=False)

    with open(f"data/manual/pokemon/ingredient_chain_of_pokemon.json", "w+", encoding="utf-8", newline="\n") as f:
        json.dump(POKEMON_ID_TO_CHAIN_TAIL_ID, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
