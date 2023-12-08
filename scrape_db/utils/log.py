import datetime
import logging
import sys


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d-%H%M%S')}.log"),
            logging.StreamHandler(sys.stdout)
        ],
    )
