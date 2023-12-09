import pandas as pd
import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module


def export_map_meta():
    with start_export_module("Map Meta"), open_sql_connection() as connection:
        df_unlocks = pd.read_sql("SELECT * FROM main_missions", connection)
        df_map = pd.read_sql("SELECT * FROM fields", connection)

        data_entries = []
        for _, row in df_map.iterrows():
            map_id = row["id"]

            favorite_berries = [
                int(berry_id)
                for berry_id in row["favorite_food_ids"].split(",")
                # Filter default berry (ID 0)
                if int(berry_id)
            ]
            unlock_count = next(
                iter(df_unlocks[df_unlocks["unlock_field_id"] == map_id]["need_library_num"].values),
                None
            )

            data_entries.append({
                "mapId": map_id,
                "berry": sorted(favorite_berries) if favorite_berries else None,
                "unlock": {
                    "type": "sleepStyle",
                    "count": unlock_count
                } if unlock_count else None
            })

        with export_to_mongo("map", "meta", data_entries) as col:
            col.create_index(
                [("mapId", pymongo.ASCENDING)],
                unique=True
            )
