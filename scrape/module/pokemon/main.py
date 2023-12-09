from scrape.module.pokemon.branch import export_pokemon_branch
from scrape.module.pokemon.info import export_pokemon_info


def export_pokemon():
    export_pokemon_info()
    export_pokemon_branch()
