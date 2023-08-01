import json

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"


with open("meal_data.json") as f:
    data = json.load(f)


def main():
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database("food")
    col_info = db.get_collection("meal")

    col_info.drop()
    col_info.create_index(
        [("id", pymongo.ASCENDING)],
        unique=True
    )
    col_info.create_index(
        [("ingredients.id", pymongo.ASCENDING)],
    )

    col_info.insert_many(data)


if __name__ == '__main__':
    main()
