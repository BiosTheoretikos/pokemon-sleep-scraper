import logging
from contextlib import contextmanager
from typing import Any, ContextManager, Iterable, Mapping

import numpy
from bson.codec_options import CodecOptions, TypeCodec, TypeRegistry
from pymongo import MongoClient
from pymongo.collection import Collection

from scrape_db.utils.env import Environment
from scrape_db.utils.snapshot import take_export_snapshot

_mongo = MongoClient(Environment.mongo_connection)


class NumpyInt64Codec(TypeCodec):
    python_type = numpy.int64
    bson_type = int

    def transform_python(self, value: numpy.int64):
        return int(value)

    def transform_bson(self, value: int):
        return numpy.int64(value)


_mongo_codec_options = CodecOptions(type_registry=TypeRegistry([NumpyInt64Codec()]))


@contextmanager
def export_to_mongo(
    db_name: str,
    collection_name: str,
    data: Iterable[Mapping[str, Any]]
) -> ContextManager[Collection[Mapping[str, Any]]]:
    logging.info("Exporting data to MongoDB collection `%s.%s`", db_name, collection_name)

    collection = _mongo.get_database(db_name).get_collection(collection_name, codec_options=_mongo_codec_options)
    yield collection

    take_export_snapshot(f"{db_name}.{collection_name.replace('/', '-')}", data)
    collection.delete_many({})
    collection.insert_many(data)
