import pandas as pd
import pymongo

from scrape.module.pokemon.const import POKEMON_ID_COLUMN
from scrape.module.pokemon.evolution import get_pokemon_evolution_chain
from scrape.module.pokemon.pickup_stats import get_df_pickup_stats
from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module
from scrape.utils.static import load_static_data


def export_pokemon_info():
    with start_export_module("Pokemon Info"), open_sql_connection() as connection:
        df_pokemon = pd.read_sql("SELECT * FROM pokemons", connection)
        df_evo = pd.read_sql("SELECT * FROM pokemon_evolutions", connection)

        df_pickup = get_df_pickup_stats(df_pokemon, connection)

        evo_chain = get_pokemon_evolution_chain(df_pokemon, df_evo)

        ingredient_chain = {
            int(pokemon_id): chain_id
            for pokemon_id, chain_id
            in load_static_data("ingredient_chain_of_pokemon").items()
        }

        data_entries = []
        for _, row in df_pokemon.iterrows():
            pokemon_id = row[POKEMON_ID_COLUMN]
            row_stats = df_pickup.loc[pokemon_id]

            data_entries.append({
                "id": pokemon_id,
                "type": row["type"],
                "specialty": row_stats["formation_tag"],
                "sleepType": row["sleep_type"],
                "stats": {
                    "frequency": row_stats["need_sec"],
                    "maxCarry": row_stats["max_own_item_count"],
                    "friendshipPoints": row["need_friend_point"],
                    "recruit": {
                        "exp": row["capture_research_exp"],
                        "shards": row["capture_coin"],
                    },
                },
                "berry": {
                    "id": row_stats["normal_berry_id"],
                    "quantity": row_stats["normal_berry_num"],
                },
                "ingredientChain": ingredient_chain[pokemon_id],
                "skill": row_stats["main_skill_id"],
                "evolution": evo_chain[pokemon_id],
                "expType": row["exp_table_type"],
                "eventType": row["event_type_name"]
            })

        with export_to_mongo("pokemon", "info", sorted(data_entries, key=lambda item: item["id"])) as col:
            col.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True
            )
