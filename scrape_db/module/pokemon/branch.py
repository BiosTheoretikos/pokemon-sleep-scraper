import pandas as pd
import pymongo

from scrape_db.module.pokemon.const import POKEMON_ID_COLUMN
from scrape_db.module.pokemon.evolution import get_pokemon_evolution_chain
from scrape_db.module.pokemon.utils import get_main_skill_id_map, get_pokemon_id_map
from scrape_db.utils.db.mongo import export_to_mongo
from scrape_db.utils.db.sqlite import open_sql_connection
from scrape_db.utils.module import start_export_module
from scrape_db.utils.static import load_static_data


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
