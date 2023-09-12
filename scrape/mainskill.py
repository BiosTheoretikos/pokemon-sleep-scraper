from bs4 import BeautifulSoup

from _functions import *

PAGE_URL = "https://www.serebii.net/pokemonsleep/skills.shtml"
MAINSKILL_URL_PREFIX = "https://serebii.net/pokemonsleep/"


with open("export/game-en.json", "r", encoding="utf-8") as f:
    game_data = json.load(f)


MAINSKILL_TO_ID = {
    name: int(mainskill_id)
    for mainskill_id, name in game_data["MainSkill"]["Name"].items()
}


def to_main_skill_effect(level, data):
    return {"level": level} | data


def to_main_skill_single_value_effect(key):
    def generate(level, values):
        return to_main_skill_effect(level, {key: int(values[0])})

    return generate


to_value_effect = to_main_skill_single_value_effect("value")


def to_range_effect(level, values):
    return to_main_skill_effect(level, {
        "range": {
            "from": int(values[0]),
            "to": int(values[1]),
        }
    })


def to_stamina_recovery_effect(target):
    def generate(level, values):
        return to_main_skill_effect(level, {"target": target, "value": int(values[0])})

    return generate


to_instant_help_effect = to_main_skill_single_value_effect("count")


def to_cooking_effect(key):
    return to_main_skill_single_value_effect(key)


def to_metronome_effect(level, _):
    return to_main_skill_effect(level, {})


def main_skill_name_to_id(name, description):
    if "Charge" not in name and "Dream Shard" not in name:
        return MAINSKILL_TO_ID[name]

    try:
        return MAINSKILL_TO_ID[f"{name}{' (#1 ~ #2)' if 'to' in description else ' (#)'}"]
    except KeyError:
        return MAINSKILL_TO_ID[name]


MAINSKILL_EFFECT_CONVERTER = {
    1: to_value_effect,
    2: to_value_effect,
    3: to_value_effect,
    4: to_stamina_recovery_effect("random"),
    5: to_range_effect,
    6: to_range_effect,
    7: to_stamina_recovery_effect("self"),
    8: to_stamina_recovery_effect("team"),
    9: to_instant_help_effect,
    10: to_cooking_effect("ingredients"),
    11: to_cooking_effect("capacity"),
    13: to_metronome_effect,
}


MAINSKILL_TYPE = {
    1: "strength",
    2: "strength",
    3: "shards",
    4: "stamina",
    5: "strength",
    6: "shards",
    7: "stamina",
    8: "stamina",
    9: "help",
    10: "cooking",
    11: "cooking",
    13: "random",
}


def main():
    mainskill_data = []

    req = send_requests([PAGE_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    _mainskill_table = soup.find_all("table", class_="dextable")[0]

    for idx, index_row in enumerate(_mainskill_table.find_all("tr")):
        if idx == 0:
            continue

        _mainskill_link = index_row.find("a")
        _mainskill_description = index_row.find_all("td")[1].text
        _mainskill_soup = BeautifulSoup(
            send_requests([f"{MAINSKILL_URL_PREFIX}{_mainskill_link['href']}"])[0].content,
            "html.parser"
        )

        _mainskill_value_table = _mainskill_soup.find_all("table", class_="dextable")[0]
        _mainskill_name = _mainskill_link.text
        main_skill_id = main_skill_name_to_id(_mainskill_name, _mainskill_description)
        main_skill_effects = []

        print(f"{_mainskill_name} (#{main_skill_id})")

        for _value_idx, _value_row in enumerate(_mainskill_value_table.find_all("tr")):
            if _value_idx == 0:
                continue

            _level, _value = _value_row.find_all("td")

            _main_skill_level = int(_level.text.split(" ", 1)[1])
            _main_skill_values = _value.text.split(" to ")
            main_skill_effects.append(
                {"type": MAINSKILL_TYPE[main_skill_id]} |
                MAINSKILL_EFFECT_CONVERTER[main_skill_id](_main_skill_level, _main_skill_values)
            )

        mainskill_data.append({
            "id": main_skill_id,
            "effects": main_skill_effects
        })

    to_json(mainskill_data, "mainskill_data")


if __name__ == '__main__':
    main()
