import os

import pandas as pd
import scipy

from rp_model.fit_options import fit_options
from rp_model.game_model import game, refresh_game_data
from rp_model.initial_guess import make_initial_guess
from rp_model.model import compute_rp, make_precomputed_columns
from rp_model.utils import download_sheet, digest, load, pack, progressive_soft_round_loop, save, unpack
from ._const import *


def pokedex_to_pickle():
    pokedex = download_sheet(RP_MODEL_FILE_ID, RP_MODEL_SHEET_IDS["pokedex"])
    pokedex = pokedex.fillna(0)
    pokedex.to_pickle(game.data_files.pokedex)

    refresh_game_data()


def residual(data, computed, unpack_info):
    def inner(x):
        return data["RP"].to_numpy() - compute_rp(x, data, computed, unpack_info)

    return inner


def get_pokemon_data():
    data_1_9 = download_sheet(RP_MODEL_FILE_ID, RP_MODEL_SHEET_IDS["data_1_9"])
    data_10_49 = download_sheet(RP_MODEL_FILE_ID, RP_MODEL_SHEET_IDS["data_10_49"])

    data = pd.concat([data_1_9, data_10_49], axis=0)
    data.dropna(subset=["Pokemon", "Level", "RP", "Nature", "MS lvl"], inplace=True)
    data.fillna(
        {"Amnt": 0, "Ing2P": 0, "Help skill bonus": 1, "RP Multiplier": 1, "ModelRP": -1, "Difference": -1},
        inplace=True
    )
    data.fillna({"Sub Skill 1": "", "Sub Skill 2": "", "Ingredient 2": "", "Source": ""}, inplace=True)

    # data above 30 requires a 2nd ingredient to be valid.
    data.drop(data.index[(data["Level"] >= 30) & (data["Amnt"] == 0.0)], inplace=True)

    # data below 30 we clear 2nd ingredient
    data.loc[data["Level"] < 30, "Amnt"] = 0.0
    data.loc[data["Level"] < 30, "Ing2P"] = 0.0
    data.loc[data["Level"] < 30, "Ingredient 2"] = ""

    # data below 25 we clear 2nd skill, and below 10 we clear the 1st
    data.loc[data["Level"] < 25, "Sub Skill 2"] = ""
    data.loc[data["Level"] < 10, "Sub Skill 1"] = ""

    # avoid a bug in RP of freshly caught mon with skill up unlocked.
    # (We now trust the bugged data is quarantined so we can use the valid data)
    # data = data[ ~( (data["Sub Skill 1"] == "Skill Level Up S") & (data["MS lvl"] == 2) )]
    # data = data[ ~( (data["Sub Skill 1"] == "Skill Level Up M") & (data["MS lvl"] == 3) )]

    # only use data known to the Pokedex (we'll update Pokedex as needed)
    data.drop(data.index[~data["Pokemon"].isin(game.game_data.pokedex["Pokemon"])], inplace=True)

    data.to_pickle(fit_options.data_file)

    return data


def get_model_opt(data, x0, unpack_info):
    # Compute per sample information about help time, nature, sub-skills etc
    computed = make_precomputed_columns(data)

    filename = fit_options.result_file(digest(data, x0))

    print(f"RP model pickle location: {filename}")
    if os.path.isfile(filename):
        print(f"RP model loaded from cache")
        return load(filename)

    opt = progressive_soft_round_loop(
        x0,
        lambda x: scipy.optimize.least_squares(
            residual(data, computed, unpack_info),
            x,
            **fit_options.least_squares_kwargs
        )
    )

    # save results and remove some stuff we don't need to save.
    if "jac" in opt:
        del opt.jac
    if "active_mask" in opt:
        del opt.active_mask
    if "fun" in opt:
        del opt.fun
    if "final_simplex" in opt:
        del opt.final_simplex

    save(filename, opt)

    return opt


def get_rp_fit_result_df():
    # Model as of https://github.com/jeancroy/RP-fit/commit/78ff158e297496e2d7562250c45537eada9390cd
    pokedex_to_pickle()

    data = get_pokemon_data()

    print(f"RP Model obtained {len(data)} Pokemon data entry")

    x0, unpack_info = pack(make_initial_guess())

    opt = get_model_opt(data, x0, unpack_info)
    sol = unpack(opt.x, unpack_info)

    df = pd.DataFrame({
        "pokemonId": game.game_data.pokedex["Pokemon ID"],
        "ingredientSplit": sol["Pokemons ing fractions"],
        "skillValue": sol["Pokemons skill products"]
    })
    df.set_index("pokemonId")

    return df
