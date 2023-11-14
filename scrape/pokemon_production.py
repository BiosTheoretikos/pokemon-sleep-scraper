import json
import time

import numpy as np

from calc.entry import get_rp_model_df

with open("data/scraped/pokemon_data.json", "r", encoding="utf-8") as f_pokemon:
    pokemon_data = json.load(f_pokemon)

POKEMON_ID_TO_MAIN_SKILL_ID = {
    data["id"]: data["skill"]
    for data in pokemon_data
}

SKILL_VALUE_IN_RP = {
    1: 400,  # Charge Strength S (#)
    2: 880,  # Charge Strength M
    3: 0,  # Dream Shard Magnet S (#)
    4: 0,  # Energizing Cheer S
    5: 0,  # Charge Strength S (#1 ~ #2)
    6: 0,  # Dream Shard Magnet S (#1 ~ #2)
    7: 0,  # Charge Energy S
    8: 0,  # Energy for Everyone S
    9: 0,  # Extra Helpful S
    10: 820.5,  # Ingredient Magnet S
    11: 959,  # Cooking Power-Up S
    12: 0,  # Type Boost S
    13: 0,  # Metronome
}

DIGIT_PRECISION = 8


def main():
    rp_model_data = get_rp_model_df()

    # Calculate skill trigger rate, if the value is available
    rp_model_skill_values = rp_model_data["pokemonId"] \
        .map(POKEMON_ID_TO_MAIN_SKILL_ID) \
        .map(SKILL_VALUE_IN_RP)
    rp_model_data["skillPercent"] = (rp_model_data["skillValue"] / rp_model_skill_values * 100) \
        .round(decimals=DIGIT_PRECISION) \
        .replace(np.Inf, None)
    # Round decimals
    rp_model_data = rp_model_data.round(decimals=DIGIT_PRECISION)
    # Add empty error fields
    # > This should be changed to actual error in the future
    rp_model_data["error"] = [{"ingredient": None, "skill": None} for _ in rp_model_data.iterrows()]
    # Select columns to export
    rp_model_data = rp_model_data[[
        "pokemonId",
        "dataCount",
        "ingredientSplit",
        "skillValue",
        "skillPercent",
        "error"
    ]]

    with open(f"data/transformed/pokemon_production.json", "w+", encoding="utf-8", newline="\n") as f_export:
        json.dump(
            {
                "data": rp_model_data.to_dict("records"),
                "lastUpdated": time.time(),
            },
            f_export,
            indent=2,
            ensure_ascii=False
        )


if __name__ == "__main__":
    main()
