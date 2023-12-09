import json
import logging
import os

from scrape.utils.env import Environment


def load_static_data(file_name: str):
    json_path = os.path.join(Environment.static_data_dir, f"{file_name}.json")
    logging.info("Loading static data at %s", json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
