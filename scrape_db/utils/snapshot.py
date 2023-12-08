import json
import logging
import os
from typing import Any, Iterable, Mapping

import numpy as np

from scrape_db.utils.env import Environment


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(obj)
        if isinstance(obj, np.int64):
            return int(obj)

        return json.JSONEncoder.default(self, obj)


def take_export_snapshot(file_name: str, data: Iterable[Mapping[str, Any]]) -> None:
    json_path = os.path.join(Environment.export_snapshot_dir, f"{file_name}.json")
    logging.info("Saving export snapshot to %s", json_path)

    with open(json_path, "w+") as f:
        json.dump(data, f, indent=2, cls=JsonEncoder)
