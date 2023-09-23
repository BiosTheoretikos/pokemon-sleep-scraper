import json

from pymongo import MongoClient

from _const import *

with open("export/game-en.json", "r", encoding="utf-8") as f_game:
    game_data = json.load(f_game)

POKEMON_NAME_TO_ID = {
    name: int(pokemon_id)
    for pokemon_id, name in game_data["PokemonName"].items()
}

with open("data/pokemon_data.json") as f:
    pokemon_data = json.load(f)

with open("transformed/ingredient_split.json") as f:
    ingredient_split = json.load(f)


ingredient_split_by_id = {
    POKEMON_NAME_TO_ID[data["Pokemon"]]: data["ing%"]
    for data in ingredient_split
}


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
        pokemon_id = pokemon["id"]
        ingredient_split_of_pokemon = ingredient_split_by_id.get(pokemon_id)

        if ingredient_split_of_pokemon:
            ingredient_split_of_pokemon /= 100
        else:
            print(f"No data for Pokemon #{pokemon_id} ({game_data['PokemonName'][str(pokemon_id)]})")

        data.append({
            "pokemonId": pokemon_id,
            "ingredientSplit": ingredient_split_of_pokemon or default_split,
        })

    col.insert_many(data)


if __name__ == "__main__":
    main()
