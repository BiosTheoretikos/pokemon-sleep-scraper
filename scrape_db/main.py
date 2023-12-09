from scrape_db.module.berry import export_berry
from scrape_db.module.ingredient import export_ingredient
from scrape_db.module.pokemon.branch import export_pokemon_branch
from scrape_db.module.pokemon.main import export_pokemon_info
from scrape_db.module.snorlax import export_snorlax
from scrape_db.module.subskill import export_subskill
from scrape_db.module.xp_shard import export_xp_shard
from scrape_db.module.xp_value import export_xp_value
from scrape_db.utils.log import init_logging


def scrape():
    init_logging()

    export_pokemon_info()
    export_pokemon_branch()
    export_berry()
    export_ingredient()
    export_subskill()
    export_snorlax()
    export_xp_value()
    export_xp_shard()
