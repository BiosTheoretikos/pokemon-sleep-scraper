from collections import defaultdict
from sqlite3 import Connection
from typing import Iterable

import pandas as pd
import pymongo
from pandas import DataFrame

from scrape.module.pokemon.utils import get_pokemon_id_map
from scrape.module.utils.rank import to_rank_object
from scrape.utils.db.mongo import export_to_mongo
from scrape.utils.db.sqlite import open_sql_connection
from scrape.utils.module import start_export_module


def get_style_id(pokemon_id: int, style_id: int) -> str | int:
    if style_id == 4:
        return "onSnorlax"

    # Ditto special handling, for mapping the style ID to match the image ID
    if pokemon_id == 132:
        match style_id:
            case 6:
                return 7
            case 7:
                return 6
            case 12:
                return 8

    return style_id


def get_sleepstyle_group_id_to_map_id(connection: Connection) -> dict[int, int]:
    df = pd.read_sql("SELECT * FROM fields", connection)

    return df.set_index("snorlax_rank_unlock_sleeping_faces_group_id")["id"].to_dict()


def get_snorlax_rank_dict(connection: Connection) -> dict[int, dict[str, int]]:
    df = pd.read_sql("SELECT * FROM snorlax_rank", connection)

    df["rank_object"] = df.apply(to_rank_object, axis="columns")
    df.set_index("id", inplace=True)

    return df["rank_object"].to_dict()


def get_df_sleepstyle_data(connection: Connection, pokemon_id_map: dict[int, int]) -> DataFrame:
    df = pd.read_sql("SELECT * FROM sleeping_faces", connection)

    df["pokemon_id"] = df["pokemon_id"].map(pokemon_id_map)

    return df


def get_df_sleepstyle_unlock(
    connection: Connection,
    snorlax_rank_ids: Iterable[int],
    sleepstyle_group_id_to_map_id: dict[int, int],
) -> DataFrame:
    df = pd.read_sql("SELECT * FROM snorlax_rank_unlock_sleeping_faces", connection)

    data = []
    for _, row in df.iterrows():
        map_id = sleepstyle_group_id_to_map_id[row["group_id"]]

        for snorlax_rank_id in snorlax_rank_ids:
            unlock_sleepstyles = row[f"snorlax_rank_unlock_face_table_ids{snorlax_rank_id}"]
            if not unlock_sleepstyles:
                continue

            for sleepstyle_id_str in str(unlock_sleepstyles).split(","):
                data.append({
                    "map_id": map_id,
                    "snorlax_rank_id": snorlax_rank_id,
                    "sleepstyle_id": int(sleepstyle_id_str),
                })

    return pd.DataFrame(data)


def export_sleepstyle():
    with start_export_module("Sleep Style"), open_sql_connection() as connection:
        sleepstyle_group_id_to_map_id = get_sleepstyle_group_id_to_map_id(connection)
        pokemon_id_map = get_pokemon_id_map(pd.read_sql("SELECT * FROM pokemons", connection))
        snorlax_rank_dict = get_snorlax_rank_dict(connection)

        df_sleepstyle_data = get_df_sleepstyle_data(connection, pokemon_id_map)
        df_sleepstyle_unlock = get_df_sleepstyle_unlock(
            connection,
            snorlax_rank_dict.keys(),
            sleepstyle_group_id_to_map_id,
        )

        data_sleep_styles_dict = defaultdict(list)
        for _, row in df_sleepstyle_data.iterrows():
            sleepstyle_id = row["id"]
            pokemon_id = row["pokemon_id"]
            style_id = row["library_sub_id"]

            data_sleep_styles_dict[pokemon_id].append({
                "style": get_style_id(pokemon_id, style_id),
                "location": [
                    {
                        "id": row_unlock["map_id"],
                        "rank": snorlax_rank_dict[row_unlock["snorlax_rank_id"]]
                    }
                    for _, row_unlock in
                    df_sleepstyle_unlock[df_sleepstyle_unlock["sleepstyle_id"] == sleepstyle_id].iterrows()
                ],
                "rewards": {
                    "exp": row["research_p"],
                    "shards": row["coin"],
                    "candy": row["research_candy_num"]
                },
            })

        data_sleep_styles_list = []
        data_sleep_styles_no_map = []

        for pokemon_id, sleep_styles in data_sleep_styles_dict.items():
            sleep_styles_in_locations = defaultdict(list)
            sleep_styles_is_unreleased = not any(sleep_style["location"] for sleep_style in sleep_styles)
            for sleep_style in sleep_styles:
                locations = sleep_style["location"]

                if not locations:
                    data_sleep_styles_no_map.append({
                        "pokemonId": pokemon_id,
                        "style": sleep_style["style"],
                        "rewards": sleep_style["rewards"],
                        "unreleased": sleep_styles_is_unreleased,
                    })
                    continue

                for sleep_style_location in locations:
                    sleep_styles_in_locations[sleep_style_location["id"]].append({
                        "style": sleep_style["style"],
                        "rank": sleep_style_location["rank"],
                        "rewards": sleep_style["rewards"]
                    })

            data_sleep_styles_list.extend(
                {
                    "pokemonId": pokemon_id,
                    "mapId": map_id,
                    "styles": sleep_styles_in_location
                }
                for map_id, sleep_styles_in_location in sleep_styles_in_locations.items()
            )

        with export_to_mongo("pokemon", "sleepStyle", data_sleep_styles_list) as col:
            col.create_index("mapId")
            col.create_index(
                [("pokemonId", pymongo.ASCENDING), ("mapId", pymongo.ASCENDING)],
                unique=True
            )

        with export_to_mongo("pokemon", "sleepStyle/noMap", data_sleep_styles_no_map) as col:
            col.create_index(
                [("pokemonId", pymongo.ASCENDING), ("style", pymongo.ASCENDING)],
                unique=True
            )
