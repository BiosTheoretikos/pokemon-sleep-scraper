from scrape.module.pokemon.branch import export_pokemon_branch
from scrape.module.pokemon.info import export_pokemon_info
from scrape.module.pokemon.production import export_pokemon_production


def export_pokemon():
    export_pokemon_info()
    export_pokemon_branch()
    export_pokemon_production()
