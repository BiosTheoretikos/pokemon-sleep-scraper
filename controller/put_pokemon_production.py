import json

from pymongo import MongoClient

from _const import *

with open("export/pokemon_production.json") as f:
    production_data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db_pokemon = client.get_database("pokemon")
col = db_pokemon.get_collection("producing")


def index():
    col.create_index("pokemonId", unique=True)


def main():
    index()

    col.delete_many({})
    col.insert_many(production_data)


if __name__ == "__main__":
    main()
