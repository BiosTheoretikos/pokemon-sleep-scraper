from scrape_db.module.berry import export_berry
from scrape_db.module.ingredient import export_ingredient
from scrape_db.module.snorlax_rank import export_snorlax_rank
from scrape_db.module.subskill import export_subskill
from scrape_db.module.xp_shard import export_xp_shard
from scrape_db.module.xp_value import export_xp_value
from scrape_db.utils.log import init_logging


def scrape():
    init_logging()

    export_berry()
    export_ingredient()
    export_subskill()
    export_snorlax_rank()
    export_xp_value()
    export_xp_shard()
