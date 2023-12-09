import json
from pathlib import Path

import grequests
from bs4 import BeautifulSoup


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(obj)

        return json.JSONEncoder.default(self, obj)


def send_requests(urls):
    reqs = [grequests.get(url) for url in urls]

    return grequests.map(reqs, size=10)


def to_json(data, filename):
    Path("./data").mkdir(parents=True, exist_ok=True)
    Path("./data/scraped").mkdir(parents=True, exist_ok=True)

    with open(f"data/scraped/{filename}.json", "w+") as f_json:
        json.dump(data, f_json, indent=2, cls=JsonEncoder)


def get_soups_of_maps():
    page_url = "https://serebii.net/pokemonsleep/researchareas.shtml"
    map_url_prefix = "https://serebii.net/pokemonsleep/"

    req = send_requests([page_url])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    for idx, index_row in enumerate(soup.find("table", class_="dextable").find_all("tr")):
        if idx < 1:
            continue

        _map_link = index_row.find("a")["href"]
        yield BeautifulSoup(
            send_requests([f"{map_url_prefix}{_map_link}"])[0].content,
            "html.parser"
        )
