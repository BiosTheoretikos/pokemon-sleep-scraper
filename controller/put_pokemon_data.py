import json
from collections import defaultdict

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"


with open("../data/pokemon_data.json") as f:
    pokemon_data = json.load(f)


def main():
    client = MongoClient(CONNECTION_STRING)
    db_pokemon = client.get_database("pokemon")
    col_info = db_pokemon.get_collection("info")
    col_sleep_style = db_pokemon.get_collection("sleepStyle")

    col_info.drop()
    col_info.create_index("id", unique=True)
    col_sleep_style.drop()
    col_sleep_style.create_index(
        [("pokemonId", pymongo.ASCENDING), ("mapId", pymongo.ASCENDING)],
        unique=True
    )

    data_info = []
    data_sleep_style = []

    for pokemon in pokemon_data:
        data_info.append({k: v for k, v in pokemon.items() if k not in ["sleepStyle", "name"]})

        pokemon_id = pokemon["id"]
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
