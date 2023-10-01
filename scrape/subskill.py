from bs4 import BeautifulSoup

from _functions import *

PAGE_URL = "https://www.serebii.net/pokemonsleep/skills.shtml"


with open("export/game-en.json", "r", encoding="utf-8") as f:
    game_data = json.load(f)


SUBSKILL_TO_ID = {
    name: int(subskill_id)
    for subskill_id, name in game_data["SubSkill"]["Name"].items()
}


# Confirmed in image assets `skill_sub_*.png`
RARITY_TO_ID = {
    "Very Rare": 3,
    "Rare": 2,
    "Common": 1,
}

# Likely datamined
# https://www.serebii.net/pokemonsleep/skills.shtml
SUBSKILL_BONUS = {
    1: {
        "exp": 14,
    },
    2: {
        "helper": 5,
    },
    3: {
        "stamina": 1.12,
    },
    4: {
        "shard": 6,
    },
    5: {
        "research": 6,
    },
    6: {
        "frequency": 7,
    },
    7: {
        "frequency": 14,
    },
    8: {
        "berryCount": 1,
    },
    9: {
        "inventory": 6,
    },
    10: {
        "inventory": 12,
    },
    11: {
        "skillLevel": 1,
    },
    12: {
        "ingredientProbability": 18,
    },
    13: {
        "ingredientProbability": 36,
    },
    14: {
        "mainSkillProbability": 18,
    },
    15: {
        "mainSkillProbability": 36,
    },
    16: {},
    17: {},
    18: {
        "skillLevel": 2,
    },
    19: {
        "inventory": 18,
    },
}

SUBSKILL_EXCLUSION = [16, 17]


def main():
    subskill_data = []

    req = send_requests([PAGE_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    _subskill_table = soup.find_all("table", class_="dextable")[1]

    for idx, index_row in enumerate(_subskill_table.find_all("tr")):
        if idx == 0:
            continue

        _name, _description, _rarity, _next = index_row.find_all("td")

        _subskill_name = _name.text
        print(_subskill_name)

        subskill_id = SUBSKILL_TO_ID[_subskill_name]

        if subskill_id in SUBSKILL_EXCLUSION:
            continue

        _rarity_children = list(_rarity.children)
        subskill_rarity = RARITY_TO_ID[_rarity_children[0].text] if _rarity_children else None
        subskill_next = SUBSKILL_TO_ID.get(_next.text, None)

        subskill_data.append({
            "id": subskill_id,
            "rarity": subskill_rarity,
            "next": subskill_next,
            "bonus": SUBSKILL_BONUS[subskill_id],
        })

    to_json(subskill_data, "subskill_data")


if __name__ == '__main__':
    main()
