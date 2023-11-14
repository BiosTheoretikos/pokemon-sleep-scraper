import json

from pymongo import MongoClient

from controller.public import CONNECTION_STRING

with open("data/transformed/pokemon_production.json") as f:
    production_data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db_pokemon = client.get_database("pokemon")
col = db_pokemon.get_collection("producing")
col_meta = db_pokemon.get_collection("producing/meta")


def index():
    col.create_index("pokemonId", unique=True)


def main():
    index()

    col.delete_many({})
    col.insert_many(production_data["data"])

    col_meta.delete_many({})
    col_meta.insert_one({
        "dataCount": sum(data["dataCount"] for data in production_data["data"]),
        "lastUpdated": production_data["lastUpdated"]
    })


if __name__ == "__main__":
    main()
