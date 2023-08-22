import json

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"

with open("transformed/evolution_chain.json") as f:
    data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("pokemon")
col = db.get_collection("evolution")


def index():
    col.create_index(
        [("pokemon", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col.delete_many({})
    col.insert_many(data)


if __name__ == '__main__':
    main()
