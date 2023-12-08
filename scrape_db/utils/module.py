import logging
import time
from contextlib import contextmanager
from typing import ContextManager


@contextmanager
def start_export_module(name: str) -> ContextManager[None]:
    _start = time.perf_counter()
    logging.info(">>> Starting export module: %s", name)
    yield
    logging.info(
        ">>> Export module of `%s` completed in %.3f seconds",
        name,
        time.perf_counter() - _start
    )
