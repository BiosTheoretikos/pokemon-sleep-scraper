from pandas import DataFrame, Series

from scrape_db.module.item.evolution import get_evolution_item_df
from scrape_db.module.pokemon.utils import get_pokemon_id_map
from scrape_db.utils.module import start_export_module

_CONDITION_PERIOD_OF_TIME_MAP = {
    "1,2,3": {
        "startHour": 6,
        "endHour": 18,
    },
    "4": {
        "startHour": 18,
        "endHour": 6,
    }
}


def get_evolution_stage(df_evo: DataFrame, pokemon_id: int) -> int:
    def get_evolution_stage_inner(pokemon_id_inner: int, stage: int) -> int:
        stages = [stage]

        for _, row in df_evo[df_evo["evolves_into"] == pokemon_id_inner].iterrows():
            stages.append(get_evolution_stage_inner(row["pokemon_id"], stage + 1))

        return max(stages)

    return get_evolution_stage_inner(pokemon_id, 1)


def get_conditions_from_row(
    df_evo_item: DataFrame,
    row: Series,
) -> list[dict]:
    conditions = []

    candy = row["need_candy"]
    if candy:
        conditions.append({
            "type": "candy",
            "count": candy,
        })

    item_ids = row["evolution_item_id"]
    if item_ids:
        for evo_item_id, evo_item_count in zip(str(item_ids).split(","), str(row["evolution_item_num"]).split(",")):
            conditions.append({
                "type": "item",
                "item": next(iter(df_evo_item[df_evo_item["item_id"] == int(evo_item_id)]["id"].values)),
                "count": int(evo_item_count),
            })

    level = row["rank"]
    if level:
        conditions.append({
            "type": "level",
            "level": level,
        })

    sleep_time = row["total_sleep_min"]
    if sleep_time:
        conditions.append({
            "type": "sleepTime",
            "hours": sleep_time / 60,
        })

    timing = row["period_of_time"]
    if timing:
        conditions.append({"type": "timing"} | _CONDITION_PERIOD_OF_TIME_MAP[str(timing)])

    return sorted(conditions, key=lambda condition: condition["type"])


def get_pokemon_evolution_chain(
    df_pokemon: DataFrame,
    df_evo: DataFrame,
) -> dict:
    df_evo_item = get_evolution_item_df()

    evo_chain = {}
    with start_export_module("Pokemon (Evolution Chain)"):
        pokemon_id_map = get_pokemon_id_map(df_pokemon)

        # Re-map IDs as the IDs in `df_evo` is using internal ID
        df_evo["pokemon_id"] = df_evo["pokemon_id"].map(pokemon_id_map)
        df_evo["evolves_into"] = df_evo["evolves_into"].map(pokemon_id_map)

        # Handle each available evolution data
        for _, row in df_evo.iterrows():
            current_id = row["pokemon_id"]
            next_id = row["evolves_into"]

            if current_id not in evo_chain:
                evo_chain[current_id] = {
                    "next": [
                        {
                            "id": next_id,
                            "conditions": get_conditions_from_row(df_evo_item, row),
                        }
                    ],
                    "stage": get_evolution_stage(df_evo, current_id),
                    "previous": next(iter(df_evo[df_evo["evolves_into"] == current_id]["pokemon_id"].values), None)
                }
                continue

            evo_chain[current_id]["next"].append({
                "id": next_id,
                "conditions": get_conditions_from_row(df_evo_item, row),
            })

        for pokedex_id in pokemon_id_map.values():
            if pokedex_id in evo_chain:
                continue

            evo_chain[pokedex_id] = {
                "next": [],
                "stage": get_evolution_stage(df_evo, pokedex_id),
                "previous": next(iter(df_evo[df_evo["evolves_into"] == pokedex_id]["pokemon_id"].values), None)
            }

    return evo_chain
