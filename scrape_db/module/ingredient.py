import pandas as pd
import pymongo

from scrape_db.utils.db.mongo import export_to_mongo
from scrape_db.utils.db.sqlite import open_sql_connection
from scrape_db.utils.module import start_export_module


def export_ingredient():
    with start_export_module("Ingredient"), open_sql_connection() as connection:
        df = pd.read_sql("SELECT * FROM cooking_foods", connection)

        data = (
            df[(df["need_cooking"] == 0) & (df["energy"] > 0)][["id", "energy", "sell_coin"]]
            .rename(columns={"sell_coin": "price"})
            .to_dict(orient="records")
        )

        with export_to_mongo("food", "ingredient", data) as col:
            col.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True
            )
