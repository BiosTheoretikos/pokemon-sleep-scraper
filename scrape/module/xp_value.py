import numpy as np
import pandas as pd
import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.extract import get_ids_from_df_column_name
from scrape.utils.module import start_export_module

_COL_PREFIX_TYPE = "need_exp_type_"


def export_xp_value():
    with start_export_module("XP (Value)"), open_sql_connection() as connection:
        df_xp = pd.read_sql("SELECT * FROM pokemon_rank_exp_table", connection)

        data_entries = []
        for type_id in get_ids_from_df_column_name(df_xp, _COL_PREFIX_TYPE):
            xp_series = df_xp[f"{_COL_PREFIX_TYPE}{type_id}"]

            data_entries.append({
                "type": type_id,
                "data": pd.DataFrame({
                    "lv": xp_series.index + 1,
                    "totalGained": xp_series,
                    "toNext": (xp_series.shift(-1) - xp_series).replace(np.nan, None),
                }).to_dict("records")
            })

        with export_to_mongo("pokemon", "xp/value", data_entries) as col:
            col.create_index(
                [("type", pymongo.ASCENDING)],
                unique=True
            )
