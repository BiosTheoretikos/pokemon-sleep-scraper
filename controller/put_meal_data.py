import json

import pymongo
from pymongo import MongoClient

from _const import *

with open("data/meal_data.json") as f:
    data = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("food")
col_info = db.get_collection("meal")


def index():
    col_info.create_index(
        [("id", pymongo.ASCENDING)],
        unique=True
    )
    col_info.create_index(
        [("ingredients.id", pymongo.ASCENDING)],
    )


def main():
    col_info.delete_many({})
    col_info.insert_many(data)


if __name__ == '__main__':
    main()
