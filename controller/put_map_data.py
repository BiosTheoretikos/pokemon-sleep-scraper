import pymongo
from pymongo import MongoClient

from _const import *

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
            10,
            18,
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
            13,
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

client = MongoClient(CONNECTION_STRING)
db = client.get_database("map")
col_info = db.get_collection("meta")


def index():
    col_info.create_index(
        [("mapId", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col_info.delete_many({})
    col_info.insert_many(data)


if __name__ == '__main__':
    main()
