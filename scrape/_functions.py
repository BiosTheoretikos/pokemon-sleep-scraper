import json

import grequests


def send_requests(urls):
    reqs = [grequests.get(url) for url in urls]

    return grequests.map(reqs, size=10)


def to_json(data, filename):
    with open(f"{filename}.json", "w+") as f_json:
        json.dump(data, f_json, indent=4)
