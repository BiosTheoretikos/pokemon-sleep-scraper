import pandas as pd
import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module


def get_meal_type(meal_id: int) -> int:
    return meal_id // 1000


def ingredient_to_dict(ingredients: str | int) -> list[dict]:
    ret = []

    if not ingredients:
        return []

    for ingredient in ingredients.split(","):
        ingredient_id_str, quantity_str = ingredient.split(":")

        ret.append({
            "id": int(ingredient_id_str),
            "quantity": int(quantity_str),
        })

    return ret


def export_meal():
    with start_export_module("Meal"), open_sql_connection() as connection:
        df = pd.read_sql("SELECT * FROM cooking_foods", connection)

        data_entries = []
        for _, row in df[(df["need_cooking"] == 1) | (df["energy"] == 0)].iterrows():
            meal_id = row["id"]

            data_entries.append({
                "id": meal_id,
                "type": get_meal_type(meal_id),
                "ingredients": ingredient_to_dict(row["cooking_stuff"])
            })

        with export_to_mongo("food", "meal", data_entries) as col:
            col.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True
            )
