import time

import numpy as np
import pandas as pd
import pymongo
from pandas import DataFrame

from calc.entry import get_rp_model_df
from scrape.module.pokemon.pickup_stats import get_df_pickup_stats
from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module

SKILL_VALUE_IN_RP = {
    # Source of 2 Charge Strength S:
    # https://cdn.discordapp.com/attachments/1181411222470537297/1181510665324728370/image.png
    1: 628.98,  # Charge Strength S (#)
    2: 0,  # Charge Strength M
    3: 0,  # Dream Shard Magnet S (#)
    4: 0,  # Energizing Cheer S
    5: 694.46,  # Charge Strength S (#1 ~ #2)
    6: 0,  # Dream Shard Magnet S (#1 ~ #2)
    7: 0,  # Charge Energy S
    8: 0,  # Energy for Everyone S
    9: 0,  # Extra Helpful S
    10: 0,  # Ingredient Magnet S
    11: 0,  # Cooking Power-Up S
    12: 0,  # Type Boost S
    13: 0,  # Metronome
}

DIGIT_PRECISION = 8


def get_rp_model_data(pokemon_to_main_skill_id: dict[int, int]) -> DataFrame:
    rp_model_data = get_rp_model_df()

    # Calculate skill trigger rate, if the value is available
    rp_model_skill_values = rp_model_data["pokemonId"] \
        .map(pokemon_to_main_skill_id) \
        .map(SKILL_VALUE_IN_RP)
    rp_model_data["skillPercent"] = (rp_model_data["skillValue"] / rp_model_skill_values * 100) \
        .round(decimals=DIGIT_PRECISION) \
        .replace(np.Inf, None)
    # Round decimals
    rp_model_data = rp_model_data.round(decimals=DIGIT_PRECISION)
    # Add empty error fields
    # > This should be changed to actual error in the future
    rp_model_data["error"] = [{"ingredient": None, "skill": None} for _ in rp_model_data.iterrows()]
    # Select columns to export
    rp_model_data = rp_model_data[[
        "pokemonId",
        "dataCount",
        "ingredientSplit",
        "skillValue",
        "skillPercent",
        "error"
    ]]

    return rp_model_data


def export_pokemon_production():
    with start_export_module("Pokemon Production"), open_sql_connection() as connection:
        pokemon_to_mainskill_id = get_df_pickup_stats(
            pd.read_sql("SELECT * FROM pokemons", connection),
            connection,
        )["main_skill_id"].to_dict()

        rp_model_data = get_rp_model_data(pokemon_to_mainskill_id)
        with export_to_mongo("pokemon", "producing", rp_model_data.to_dict("records")) as col:
            col.create_index(
                [("pokemonId", pymongo.ASCENDING)],
                unique=True
            )

        production_meta = [{
            "dataCount": int(rp_model_data["dataCount"].sum()),
            "lastUpdated": time.time()
        }]
        with export_to_mongo("pokemon", "producing/meta", production_meta):
            pass
