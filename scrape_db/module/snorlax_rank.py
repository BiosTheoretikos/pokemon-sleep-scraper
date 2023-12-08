import pandas as pd
import pymongo

from scrape_db.utils.db import export_to_mongo, open_sql_connection
from scrape_db.utils.extract import get_string_key_id_extractor
from scrape_db.utils.module import start_export_module


_COL_PREFIX_STRENGTH_REQ = "need_energy_field_"


def export_snorlax_rank():
    extract_field_id_from_energy = get_string_key_id_extractor(_COL_PREFIX_STRENGTH_REQ)

    with start_export_module("Snorlax Rank"), open_sql_connection() as connection:
        df = pd.read_sql("SELECT * FROM snorlax_rank", connection)

        map_ids = [
            extract_field_id_from_energy(col_name)
            for col_name in df.columns
            if col_name.startswith(_COL_PREFIX_STRENGTH_REQ)
        ]

        data_entries = {map_id: [] for map_id in map_ids}
        for _, row in df.iterrows():
            rank = {
                "title": row["main_rank"],
                "number": row["sub_rank"],
            }

            for map_id in map_ids:
                data_entries[map_id].append({
                    "rank": rank,
                    "energy": row[f"{_COL_PREFIX_STRENGTH_REQ}{map_id}"]
                })

        data = [
            {"mapId": map_id, "data": entry}
            for map_id, entry in data_entries.items()
        ]

        with export_to_mongo("snorlax", "rank", data) as col:
            col.create_index(
                [("mapId", pymongo.ASCENDING)],
                unique=True
            )
