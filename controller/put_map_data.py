import json

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"

data = [
    {
        "mapId": 1,
        "berry": None,
        "unlock": None
    },
    {
        "mapId": 2,
        "berry": [
            3,
            8,
            10
        ],
        "unlock": {
            "type": "sleepStyle",
            "count": 20,
        }
    },
    {
        "mapId": 3,
        "berry": [
            2,
            9,
            13
        ],
        "unlock": {
            "type": "sleepStyle",
            "count": 70,
        }
    },
    {
        "mapId": 4,
        "berry": [
            1,
            6,
            16,
        ],
        "unlock": {
            "type": "sleepStyle",
            "count": 150,
        }
    }
]


def main():
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database("map")
    col_info = db.get_collection("meta")

    col_info.drop()
    col_info.create_index(
        [("mapId", pymongo.ASCENDING)],
        unique=True
    )

    col_info.insert_many(data)


if __name__ == '__main__':
    main()
