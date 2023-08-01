import json

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"


with open("snorlax_rank.json") as f:
    snorlax_rank = json.load(f)


with open("snorlax_reward.json") as f:
    snorlax_reward = json.load(f)


def main():
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database("snorlax")

    col_rank = db.get_collection("rank")
    col_rank.drop()
    col_rank.create_index(
        [("mapId", pymongo.ASCENDING)],
        unique=True
    )
    col_rank.insert_many(snorlax_rank)

    col_reward = db.get_collection("reward")
    col_reward.drop()
    col_reward.create_index(
        [("rank", pymongo.ASCENDING)],
        unique=True
    )
    col_reward.insert_many(snorlax_reward)


if __name__ == '__main__':
    main()
