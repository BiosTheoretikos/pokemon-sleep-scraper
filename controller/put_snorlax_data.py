import json

import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:23015"

with open("data/snorlax_rank.json") as f:
    snorlax_rank = json.load(f)

with open("data/snorlax_reward.json") as f:
    snorlax_reward = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("snorlax")
col_rank = db.get_collection("rank")
col_reward = db.get_collection("reward")


def index():
    col_rank.create_index(
        [("mapId", pymongo.ASCENDING)],
        unique=True
    )
    col_reward.create_index(
        [("rank", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    col_rank.delete_many({})
    col_rank.insert_many(snorlax_rank)

    col_reward.delete_many({})
    col_reward.insert_many(snorlax_reward)


if __name__ == '__main__':
    main()
