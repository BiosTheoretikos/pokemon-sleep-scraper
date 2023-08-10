import json

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"

with open("data/berry_data.json") as f:
    data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("food")
col_info = db.get_collection("berry")


def index():
    col_info.create_index(
        [("id", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col_info.delete_many({})
    col_info.insert_many(data)


if __name__ == '__main__':
    main()
