from bs4 import BeautifulSoup

from _const import *
from _functions import *

PAGE_URL = "https://serebii.net/pokemonsleep/snorlaxratings.shtml"


def main():
    snorlax_rank_data = {1: [], 2: []}
    rewards = []

    req = send_requests([PAGE_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    for idx, index_row in enumerate(soup.find("table", class_="dextable").find_all("tr")):
        if idx < 2:
            continue

        rank, energy_1, _, energy_2, __, shards = index_row.find_all("td")
        _rank_title, _rank_number = rank.text.split(" ")
        rank = {
            "title": MAP_TITLE_TO_ID[_rank_title],
            "number": int(_rank_number),
        }
        energy_1 = int(energy_1.text.replace(",", ""))
        energy_2 = int(energy_2.text.replace(",", ""))
        shards = int(shards.text.split(" ")[0].replace(",", ""))

        snorlax_rank_data[1].append({"rank": rank, "energy": energy_1})
        snorlax_rank_data[2].append({"rank": rank, "energy": energy_2})
        rewards.append({"rank": rank, "shard": shards})

    to_json(
        [{"mapId": map_id, "data": data} for map_id, data in snorlax_rank_data.items()],
        "snorlax_rank"
    )
    to_json(rewards, "snorlax_reward")


if __name__ == "__main__":
    main()
