import pandas as pd
from pandas import DataFrame

from scrape_db.enum.item_type import ItemType
from scrape_db.utils.db import open_sql_connection


def get_evolution_item_df() -> DataFrame:
    with open_sql_connection() as connection:
        return pd.read_sql(
            f"SELECT * FROM item_name_data WHERE item_type = {ItemType.EVOLUTION_ITEM.value}",
            connection
        )
