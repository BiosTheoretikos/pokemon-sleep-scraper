from typing import Literal

import pandas as pd
import pymongo
from pandas import Series

from scrape_db.utils.db.mongo import export_to_mongo
from scrape_db.utils.db.sqlite import open_sql_connection
from scrape_db.utils.extract import get_string_key_id_extractor
from scrape_db.utils.module import start_export_module

# This maps to the type of `SubSkillBonus` in UI
SubskillEffectType = Literal[
    "exp",
    "helper",
    "stamina",
    "shard",
    "research",
    "frequency",
    "berryCount",
    "inventory",
    "skillLevel",
    "ingredientProbability",
    "mainSkillProbability",
]

_bonus_type_mapping: dict[int, SubskillEffectType] = {
    12: "exp",
    18: "helper",
    4: "stamina",
    6: "shard",
    5: "research",
    17: "frequency",
    19: "berryCount",
    20: "inventory",
    21: "skillLevel",
    16: "ingredientProbability",
    14: "mainSkillProbability",
}


def get_effect_value(effect_type: SubskillEffectType, value: int | float):
    # The website was using web scraping for getting the data,
    # therefore the data doesn't conform whatever actually is in the database,
    # requiring manual remapping
    if effect_type in ("berryCount", "inventory", "skillLevel"):
        return value

    if effect_type == "stamina":
        return 1 + value / 1000

    return value / 10


def get_effect(row: Series) -> dict[str, int]:
    effect_type_num: int = row["bonus_type"]
    effect_type: SubskillEffectType | None = _bonus_type_mapping.get(effect_type_num)

    if effect_type is None:
        raise RuntimeError(f"Subskill with name key of {row['name']} got unhandled effect type {effect_type_num}")

    return {
        effect_type: get_effect_value(effect_type, row["bonus_num"])
    }


def export_subskill():
    extract_id = get_string_key_id_extractor("md_pokemon_rankup_bonus_name_")

    with start_export_module("Subskill"), open_sql_connection() as connection:
        df = pd.read_sql("SELECT * FROM pokemon_rankup_bonus", connection)

        data_entries = []
        for _, row in df.iterrows():
            id_next = None
            _id_next_original = row["upgrade_to"]
            if _id_next_original:
                id_next = extract_id(df[df["id"] == _id_next_original].iloc[0]["name"])

            data_entries.append({
                # Not using builtin ID because the text ID of 18, 19 is used on the website,
                # but it's 16, 17 internally
                "id": extract_id(row["name"]),
                "rarity": row["rarity"],
                "next": id_next,
                "bonus": get_effect(row),
            })

        with export_to_mongo("skill", "sub", data_entries) as col:
            col.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True
            )
