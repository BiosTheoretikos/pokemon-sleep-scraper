import json

import pymongo
from pymongo import MongoClient

from _const import *

with open("data/manual/pokemon/ingredient_chain.json") as f:
    data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("pokemon")
col_info = db.get_collection("ingredient")


def index():
    col_info.create_index(
        [("chainId", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col_info.delete_many({})
    col_info.insert_many(data)


if __name__ == '__main__':
    main()
