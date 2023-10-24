import json
from collections import defaultdict

import pymongo
from pymongo import MongoClient

from _const import *

with open("data/scraped/pokemon_data.json") as f:
    pokemon_data = json.load(f)

with open("data/manual/pokemon/ingredient_chain_of_pokemon.json") as f:
    ingredient_chain_dict = json.load(f)

ingredient_chain_dict = {int(pokemon_id): chain_id for pokemon_id, chain_id in ingredient_chain_dict.items()}

with open("data/manual/pokemon/evolution_chain.json") as f:
    evolution_chain_dict = json.load(f)

client = MongoClient(CONNECTION_STRING)
db_pokemon = client.get_database("pokemon")
col_info = db_pokemon.get_collection("info")
col_sleep_style = db_pokemon.get_collection("sleepStyle")


def index():
    col_info.create_index("id", unique=True)
    col_info.create_index("ingredients.fixed")
    col_info.create_index("ingredients.random")
    col_sleep_style.create_index("mapId")
    col_sleep_style.create_index(
        [("pokemonId", pymongo.ASCENDING), ("mapId", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col_info.delete_many({})
    col_sleep_style.delete_many({})

    data_info = []
    data_sleep_style = []

    for pokemon in pokemon_data:
        pokemon_id = pokemon["id"]

        pokemon["ingredientChain"] = ingredient_chain_dict[pokemon_id]
        pokemon["evolution"] = evolution_chain_dict[str(pokemon_id)]

        data_info.append({k: v for k, v in pokemon.items() if k not in ["sleepStyle", "name"]})

        pokemon_sleep_style_at_location = defaultdict(list)
        for pokemon_sleep_style in pokemon["sleepStyle"]:
            for sleep_style_location in pokemon_sleep_style["location"]:
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


if __name__ == '__main__':
    main()
