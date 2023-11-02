import json

from pymongo import MongoClient

from controller.public import CONNECTION_STRING

with open("data/manual/pokemon/branch.json") as f:
    branch_dict = json.load(f)

client = MongoClient(CONNECTION_STRING)
db_pokemon = client.get_database("pokemon")
col = db_pokemon.get_collection("branch")


def index():
    col.create_index("pokemonId", unique=True)
    col.create_index("branches")


def to_data_list():
    return [
        {
            "pokemonId": int(pokemon_id),
            "branches": branch_ids,
        }
        for pokemon_id, branch_ids in branch_dict.items()
    ]


def main():
    index()

    col.delete_many({})
    col.insert_many(to_data_list())


if __name__ == "__main__":
    main()
