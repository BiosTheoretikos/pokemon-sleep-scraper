from scrape.module.berry import export_berry
from scrape.module.ingredient import export_ingredient
from scrape.module.map import export_map_meta
from scrape.module.pokemon.branch import export_pokemon_branch
from scrape.module.pokemon.main import export_pokemon_info
from scrape.module.snorlax import export_snorlax
from scrape.module.subskill import export_subskill
from scrape.module.xp_shard import export_xp_shard
from scrape.module.xp_value import export_xp_value
from scrape.utils.log import init_logging


def scrape():
    init_logging()

    export_pokemon_info()
    export_pokemon_branch()

    export_berry()
    export_ingredient()

    export_subskill()

    export_map_meta()
    export_snorlax()

    export_xp_value()
    export_xp_shard()
