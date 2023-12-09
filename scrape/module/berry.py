import pandas as pd
import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module


def export_berry():
    with start_export_module("Berry"), open_sql_connection() as connection:
        data = (
            pd.read_sql("SELECT * FROM berry_energy", connection)
            .drop("id", axis="columns")
            .rename(columns={"berry_id": "id"})
            .groupby(["id"])
            .apply(lambda x: x[["rank", "energy"]].rename(columns={"rank": "lv"}).to_dict("records"))
            .reset_index()
            .rename(columns={0: "energy"})
            .to_dict(orient="records")
        )

        with export_to_mongo("food", "berry", data) as col:
            col.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True
            )
