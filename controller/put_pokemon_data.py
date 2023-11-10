import json
from collections import defaultdict

import pymongo
from pymongo import MongoClient

from controller.public import CONNECTION_STRING

with open("data/scraped/pokemon_data.json") as f:
    pokemon_data = json.load(f)

with open("data/manual/pokemon/ingredient_chain.json") as f:
    ingredient_chain_list = json.load(f)

ingredient_chain_list = {int(entry["chainId"]) for entry in ingredient_chain_list}

with open("data/manual/pokemon/ingredient_chain_of_pokemon.json") as f:
    ingredient_chain_of_pokemon_dict = json.load(f)

ingredient_chain_of_pokemon_dict = {
    int(pokemon_id): chain_id for pokemon_id, chain_id
    in ingredient_chain_of_pokemon_dict.items()
}

with open("data/manual/pokemon/evolution_chain.json") as f:
    evolution_chain_dict = json.load(f)

client = MongoClient(CONNECTION_STRING)
db_pokemon = client.get_database("pokemon")
col_info = db_pokemon.get_collection("info")
col_sleep_style = db_pokemon.get_collection("sleepStyle")
col_sleep_style_no_map = db_pokemon.get_collection("sleepStyle/noMap")


def index():
    col_info.create_index("id", unique=True)
    col_info.create_index("ingredients.fixed")
    col_info.create_index("ingredients.random")
    col_sleep_style.create_index("mapId")
    col_sleep_style.create_index(
        [("pokemonId", pymongo.ASCENDING), ("mapId", pymongo.ASCENDING)],
        unique=True
    )
    col_sleep_style_no_map.create_index(
        [("pokemonId", pymongo.ASCENDING), ("style", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col_info.delete_many({})
    col_sleep_style.delete_many({})
    col_sleep_style_no_map.delete_many({})

    data_info = []
    data_sleep_style = []
    data_sleep_style_no_map = []

    for pokemon in pokemon_data:
        pokemon_id = pokemon["id"]

        ingredient_chain_id = ingredient_chain_of_pokemon_dict[pokemon_id]

        if ingredient_chain_id not in ingredient_chain_list:
            raise RuntimeError(
                f"Ingredient Chain ID #{ingredient_chain_id} of Pokemon #{pokemon_id} does not have data"
            )

        pokemon["ingredientChain"] = ingredient_chain_id
        pokemon["evolution"] = evolution_chain_dict[str(pokemon_id)]

        data_info.append({k: v for k, v in pokemon.items() if k not in ["sleepStyle", "name"]})

        pokemon_sleep_style_at_location = defaultdict(list)
        pokemon_sleep_style_unreleased = not any(
            pokemon_sleep_style["location"] for pokemon_sleep_style in pokemon["sleepStyle"]
        )
        for pokemon_sleep_style in pokemon["sleepStyle"]:
            locations = pokemon_sleep_style["location"]

            if not locations:
                data_sleep_style_no_map.append({
                    "pokemonId": pokemon_id,
                    "style": pokemon_sleep_style["style"],
                    "rewards": pokemon_sleep_style["rewards"],
                    "unreleased": pokemon_sleep_style_unreleased,
                })
                continue

            for sleep_style_location in locations:
                pokemon_sleep_style_at_location[sleep_style_location["id"]].append({
                    "style": pokemon_sleep_style["style"],
                    "rank": sleep_style_location["rank"],
                    "rewards": pokemon_sleep_style["rewards"]
                })

        for location_id, sleep_styles in pokemon_sleep_style_at_location.items():
            data_sleep_style.append({
                "pokemonId": pokemon_id,
                "mapId": location_id,
                "styles": sleep_styles
            })

    col_info.insert_many(data_info)
    col_sleep_style.insert_many(data_sleep_style)
    col_sleep_style_no_map.insert_many(data_sleep_style_no_map)


if __name__ == '__main__':
    main()
