import json

import pymongo
from pymongo import MongoClient

from _const import *

with open("data/scraped/subskill_data.json") as f:
    data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("skill")
col = db.get_collection("sub")


def index():
    col.create_index(
        [("id", pymongo.ASCENDING)],
        unique=True
    )


def main():
    col.delete_many({})
    col.insert_many(data)


if __name__ == '__main__':
    main()
