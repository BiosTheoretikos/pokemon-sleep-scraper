import pandas as pd

from scrape_db.utils.db import export_to_mongo, open_sql_connection
from scrape_db.utils.module import start_export_module


def export_xp_shard():
    with start_export_module("XP (Shard)"), open_sql_connection() as connection:
        df_shard = pd.read_sql("SELECT * FROM coin_per_candy_table", connection)

        data = [{
            "data": df_shard["need_coin_per_candy"].to_list(),
        }]

        with export_to_mongo("pokemon", "xp/shard", data):
            pass
