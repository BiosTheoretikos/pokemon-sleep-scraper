import pymongo

from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.module import start_export_module
from scrape.utils.static import load_static_data


def export_pokemon_ingredient_chain():
    with (
        start_export_module("Pokemon Ingredient Chain"),
        export_to_mongo(
            "pokemon",
            "ingredient",
            load_static_data("ingredient_chain")
        ) as col
    ):
        col.create_index(
            [("chainId", pymongo.ASCENDING)],
            unique=True
        )
