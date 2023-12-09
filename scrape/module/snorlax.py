import pandas as pd
import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.extract import get_ids_from_df_column_name
from scrape.utils.module import start_export_module

_COL_PREFIX_STRENGTH_REQ = "need_energy_field_"

_COL_PREFIX_REWARD_SHARDS = "reward_coin_field_"


def export_snorlax():
    with start_export_module("Snorlax"), open_sql_connection() as connection:
        df_snorlax = pd.read_sql("SELECT * FROM snorlax_rank", connection)
        df_map = pd.read_sql("SELECT * FROM fields", connection)

        map_ids = [
            map_id for map_id in get_ids_from_df_column_name(df_snorlax, _COL_PREFIX_STRENGTH_REQ)
            if map_id in df_map["id"].values
        ]

        data_entries = {map_id: [] for map_id in map_ids}
        for _, row in df_snorlax.iterrows():
            rank = {
                "title": row["main_rank"],
                "number": row["sub_rank"],
            }

            for map_id in map_ids:
                data_entries[map_id].append({
                    "rank": rank,
                    "energy": row[f"{_COL_PREFIX_STRENGTH_REQ}{map_id}"],
                    "rewardShard": row[f"{_COL_PREFIX_REWARD_SHARDS}{map_id}"],
                })

        data = [
            {"mapId": map_id, "data": entry}
            for map_id, entry in data_entries.items()
        ]

        with export_to_mongo("map", "snorlax", data) as col:
            col.create_index(
                [("mapId", pymongo.ASCENDING)],
                unique=True
            )
