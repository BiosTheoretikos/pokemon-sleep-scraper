from pandas import DataFrame

from scrape.module.pokemon.const import POKEMON_ID_COLUMN
from scrape.utils.extract import get_string_key_id_extractor


def get_pokemon_id_map(df_pokemon: DataFrame) -> dict[int, int]:
    pokemon_id_map = df_pokemon[["id", POKEMON_ID_COLUMN]].set_index("id").to_dict()[POKEMON_ID_COLUMN]

    # Check for ID uniqueness
    assert len(set(pokemon_id_map.keys())) == len(set(pokemon_id_map.values()))

    return pokemon_id_map


def get_main_skill_id_map(df_main_skill: DataFrame) -> dict:
    extract_id = get_string_key_id_extractor("md_pokemon_main_skills_name_")
    df_ret = df_main_skill[["id", "name"]].set_index("id").rename(columns={"name": "skill_id"})
    df_ret["skill_id"] = df_ret["skill_id"].map(extract_id)

    return df_ret.to_dict()["skill_id"]
