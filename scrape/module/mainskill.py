import math

import pandas as pd
import pymongo
from pandas import Series

from scrape.enum.main_skill_effect import MainSkillEffect
from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.extract import get_ids_from_df_column_name, get_string_key_id_extractor
from scrape.utils.module import start_export_module


def to_effect_at_level(row: Series, effect_type: MainSkillEffect, level: int) -> dict:
    base_value = row[f"level_{level}"]
    range_min_mult = row["random_range_lower"] / 10000
    range_max_mult = row["random_range_upper"] / 10000

    effect = {
        "type": effect_type.to_type_str(),
        "level": level,
    }
    match effect_type:
        case MainSkillEffect.STRENGTH_FIXED | MainSkillEffect.SHARDS_FIXED:
            effect |= {
                "value": base_value,
            }
        case MainSkillEffect.STRENGTH_RANDOM | MainSkillEffect.SHARED_RANDOM:
            effect |= {
                "range": {
                    "from": math.ceil(base_value * range_min_mult),
                    "to": math.ceil(base_value * range_max_mult),
                }
            }
        case MainSkillEffect.RECOVERY_SELF | MainSkillEffect.RECOVERY_RANDOM | MainSkillEffect.RECOVERY_TEAM:
            effect |= {
                "target": effect_type.to_target(),
                "value": base_value / 10,
            }
        case MainSkillEffect.HELP:
            effect |= {
                "count": base_value,
            }
        case MainSkillEffect.INGREDIENT:
            effect |= {
                "ingredients": base_value,
            }
        case MainSkillEffect.POT_CAPACITY:
            effect |= {
                "capacity": base_value,
            }
        case MainSkillEffect.METRONOME:
            pass
        case _:
            raise RuntimeError(f"Unhandled main skill effect type: {effect_type}")

    return effect


def to_effect_at_levels(row: Series, levels: list[int]) -> list[dict]:
    effect_type = MainSkillEffect(row["effect_type"])

    return [to_effect_at_level(row, effect_type, level) for level in levels]


def export_main_skill():
    extract_id = get_string_key_id_extractor("md_pokemon_main_skills_name_")

    with start_export_module("Main Skill"), open_sql_connection() as connection:
        df = pd.read_sql("SELECT * FROM pokemon_main_skills", connection)

        levels = get_ids_from_df_column_name(df, "level_", exclude_suffix="_formation_power")

        data_entries = []
        for _, row in df.iterrows():
            skill_id = extract_id(row["name"])

            data_entries.append({
                "id": skill_id,
                "effects": to_effect_at_levels(row, levels),
            })

        with export_to_mongo("skill", "main", data_entries) as col:
            col.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True,
            )
