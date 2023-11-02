from types import SimpleNamespace

import pandas as pd


def refresh_game_data():
    game.game_data = SimpleNamespace(**dict([(k, pd.read_pickle(v)) for k, v in vars(game.data_files).items()]))


game = SimpleNamespace()

game.natures = SimpleNamespace(
    soh_effect=0.1,
    ing_effect=0.2,
    msc_effect=0.2,
    energy_effect=0.08,
)

game.subskills = SimpleNamespace(
    help_s_effect=0.07,
    help_m_effect=0.14,
    ing_s_effect=0.18,
    ing_m_effect=0.36,
    trigger_s_effect=0.18,
    trigger_m_effect=0.36,
)

game.data_files = SimpleNamespace(
    natures="./data/rp_model/data/natures.pickle",
    subskills="./data/rp_model/data/subskills.pickle",
    mainskills="./data/rp_model/data/mainskills.pickle",
    pokedex="./data/rp_model/data/pokedex.pickle",
)

# read all the data files here
refresh_game_data()

game.subskills.bonus_names = (
    game.game_data.subskills["Subskill"][game.game_data.subskills["RP Bonus Estimate"] > 0].tolist()
)
