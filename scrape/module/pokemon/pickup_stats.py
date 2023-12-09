from sqlite3 import Connection

import pandas as pd
from pandas import DataFrame

from scrape.module.pokemon.utils import get_main_skill_id_map, get_pokemon_id_map


def get_df_pickup_stats(
    df_pokemon: DataFrame,
    connection: Connection,
) -> DataFrame:
    df_pickup = pd.read_sql("SELECT * FROM pokemon_pickup_status", connection)
    df_pickup["pokemon_id"] = df_pickup["pokemon_id"].map(get_pokemon_id_map(df_pokemon))
    df_pickup.set_index("pokemon_id", inplace=True)

    main_skill_id_map = get_main_skill_id_map(pd.read_sql("SELECT * FROM pokemon_main_skills", connection))
    df_pickup["main_skill_id"] = df_pickup["main_skill_id"].map(main_skill_id_map)

    return df_pickup
