from scrape_db.module.berry import export_berry
from scrape_db.utils.log import init_logging


def scrape():
    init_logging()
    export_berry()
