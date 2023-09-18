import json

from pymongo import MongoClient

from _const import *

with open("data/pokemon_data.json") as f:
    pokemon_data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db_pokemon = client.get_database("pokemon")
col = db_pokemon.get_collection("producing")

default_split = 0.2


def index():
    col.create_index("pokemonId", unique=True)


def main():
    index()

    col.delete_many({})

    data = []

    for pokemon in pokemon_data:
        data.append({
            "pokemonId": pokemon["id"],
            "ingredientSplit": default_split,
        })

    col.insert_many(data)


if __name__ == "__main__":
    main()
