import logging
import sqlite3
from contextlib import contextmanager
from sqlite3 import Connection
from typing import Any, ContextManager, Iterable, Mapping

from pymongo import MongoClient
from pymongo.collection import Collection

from scrape_db.utils.env import Environment
from scrape_db.utils.snapshot import take_export_snapshot


@contextmanager
def open_sql_connection() -> ContextManager[Connection]:
    logging.info("Opening SQLite connection from file: %s", Environment.master_data_path)

    connection = sqlite3.connect(Environment.master_data_path)
    yield connection

    connection.close()


_mongo = MongoClient(Environment.mongo_connection)


@contextmanager
def export_to_mongo(
    db_name: str,
    collection_name: str,
    data: Iterable[Mapping[str, Any]]
) -> ContextManager[Collection[Mapping[str, Any]]]:
    logging.info("Exporting data to MongoDB collection `%s.%s`", db_name, collection_name)

    collection = _mongo.get_database(db_name).get_collection(collection_name)
    yield collection

    take_export_snapshot(f"{db_name}.{collection_name.replace('/', '-')}", data)
    # collection.delete_many({})
    # collection.insert_many(data)
