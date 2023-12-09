import os
from pathlib import Path


class Environment:
    master_data_path = os.path.abspath(
        os.environ.get("PKS_DB_MASTERDATA_PATH", "./data/assets/db/store/masterdata_server.sqlite")
    )
    export_snapshot_dir = os.path.abspath(
        os.environ.get("PKS_DB_EXPORT_SNAPSHOT_DIR", "./data/snapshot")
    )
    static_data_dir = os.path.abspath(
        os.environ.get("PKS_STATIC_DATA_DIR", "./data/static")
    )
    mongo_connection = os.environ.get("PKS_MONGODB_URI", "mongodb://localhost:23015")


Path(Environment.export_snapshot_dir).mkdir(parents=True, exist_ok=True)
