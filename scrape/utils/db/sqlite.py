import logging
import sqlite3
from contextlib import contextmanager
from sqlite3 import Connection
from typing import ContextManager

from scrape.utils.env import Environment


@contextmanager
def open_sql_connection() -> ContextManager[Connection]:
    logging.info("Opening SQLite connection from file: %s", Environment.master_data_path)

    connection = sqlite3.connect(Environment.master_data_path)
    yield connection

    connection.close()
