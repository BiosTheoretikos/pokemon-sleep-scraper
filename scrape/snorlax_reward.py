from bs4 import BeautifulSoup

from _const import *
from _functions import *

PAGE_URL = "https://serebii.net/pokemonsleep/snorlaxratings.shtml"


def main():
    rewards = []

    req = send_requests([PAGE_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    for idx, index_row in enumerate(soup.find("table", class_="dextable").find_all("tr")):
        if idx < 2:
            continue

        rank, _, _, _, _, _, _, shards = index_row.find_all("td")
        _rank_title, _rank_number = rank.text.split(" ")
        rank = {
            "title": MAP_TITLE_TO_ID[_rank_title],
            "number": int(_rank_number),
        }
        shards = int(shards.text.split(" ")[0].replace(",", ""))

        rewards.append({"rank": rank, "shard": shards})

    to_json(rewards, "snorlax_reward")


if __name__ == "__main__":
    main()
