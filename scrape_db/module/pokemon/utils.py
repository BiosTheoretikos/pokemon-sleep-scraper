from pandas import DataFrame

from scrape_db.module.pokemon.const import POKEMON_ID_COLUMN


def get_pokemon_id_map(df_pokemon: DataFrame) -> dict:
    pokemon_id_map = df_pokemon[["id", POKEMON_ID_COLUMN]].set_index("id").to_dict()[POKEMON_ID_COLUMN]
    pokedex_ids = set(pokemon_id_map.values())

    # Check for ID uniqueness
    assert len(set(pokemon_id_map.keys())) == len(pokedex_ids)

    return pokemon_id_map
