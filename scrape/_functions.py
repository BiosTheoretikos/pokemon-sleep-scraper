import json

import grequests


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(obj)

        return json.JSONEncoder.default(self, obj)


def send_requests(urls):
    reqs = [grequests.get(url) for url in urls]

    return grequests.map(reqs, size=10)


def to_json(data, filename):
    with open(f"data/{filename}.json", "w+") as f_json:
        json.dump(data, f_json, indent=4, cls=JsonEncoder)
