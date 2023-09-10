import json

import pymongo
from pymongo import MongoClient

from _const import *

with open("transformed/pokemon_xp.json") as f:
    data_xp = json.load(f)

with open("transformed/pokemon_xp_multiplier.json") as f:
    data_mult = json.load(f)

client = MongoClient(CONNECTION_STRING)
db = client.get_database("pokemon")
col_xp = db.get_collection("xp")
col_xp_mult = db.get_collection("xpMultiplier")


def index():
    col_xp.create_index(
        [("lv", pymongo.ASCENDING)],
        unique=True
    )
    col_xp_mult.create_index(
        [("pokemon", pymongo.ASCENDING)],
        unique=True
    )


def main():
    index()

    data_xp_with_total = []
    total_gained = 0
    for data_xp_single in data_xp:
        data_xp_with_total.append(data_xp_single | {"totalGained": total_gained})
        total_gained += data_xp_single["toNext"]

    col_xp.delete_many({})
    col_xp.insert_many(data_xp_with_total)
    col_xp_mult.delete_many({})
    col_xp_mult.insert_many(data_mult)


if __name__ == '__main__':
    main()
