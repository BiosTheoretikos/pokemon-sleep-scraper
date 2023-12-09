import pandas as pd
import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module


def export_pokemon_branch():
    with start_export_module("Pokemon Branch"), open_sql_connection() as connection:
        df_pokemon = pd.read_sql("SELECT * FROM pokemons", connection)

        data = (
            df_pokemon[df_pokemon["image_id"] != df_pokemon["pokedex_order_id"]][["image_id", "pokedex_order_id"]]
            .rename(columns={"pokedex_order_id": "pokemonId"})
            .groupby(["pokemonId"])
            .apply(lambda x: x[["image_id"]].to_dict("list")["image_id"])
            .reset_index()
            .rename(columns={0: "branches"})
            .to_dict(orient="records")
        )

        with export_to_mongo("pokemon", "branch", data) as col:
            col.create_index(
                [("pokemonId", pymongo.ASCENDING)],
                unique=True
            )
