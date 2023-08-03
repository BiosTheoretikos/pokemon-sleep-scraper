import warnings
from collections import defaultdict

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

from _const import *
from _functions import *

INDEX_URL = "https://www.serebii.net/pokemonsleep/pokemon.shtml"

POKEMON_URL_PREFIX = "https://www.serebii.net/"

with open("../transformed/sleep_strings.json", "r", encoding="utf-8") as f:
    MAP_OF_TO_SLEEP_STYLE_ID = {}
    for key, value in json.load(f).items():
        if key == "onSnorlax":
            continue

        _pokemon_id, _style_type = key.split("-")
        _pokemon_id = int(_pokemon_id)
        _style_type = int(_style_type)

        if _pokemon_id not in MAP_OF_TO_SLEEP_STYLE_ID:
            MAP_OF_TO_SLEEP_STYLE_ID[_pokemon_id] = {}

        MAP_OF_TO_SLEEP_STYLE_ID[_pokemon_id][value] = _style_type


def get_sleep_style_id(poke, name):
    if name == "Atop-Belly Sleep":
        return "onSnorlax"

    return MAP_OF_TO_SLEEP_STYLE_ID[poke][name]


def get_main_skill_id(name, desc):
    if name == "Charge Strength S":
        if "anywhere" in desc:
            return 5

        return 1

    if name == "Dream Shard Magnet S":
        if "to" in desc:
            return 6

        return 3

    return MAP_SKILL_NAME_TO_ID[name]


def transform_stats(stats):
    frequency = stats["Base Frequency"]
    frequency_h, frequency_m, frequency_s = frequency.split(":")

    return {
        "frequency": int(frequency_h) * 3600 + int(frequency_m) * 60 + int(frequency_s),
        "maxCarry": stats["Carry Limit"],
        "friendshipPoints": stats["Friendship Points Needed"],
        "recruit": {
            "exp": stats["Recruit Experience"],
            "shards": stats["Recruit Shards"]
        }
    }


def main():
    pokemon_data = []
    pokemon_evo_chain: defaultdict[int, defaultdict[int, list]] = defaultdict(lambda: defaultdict(list))

    req = send_requests([INDEX_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    for idx, index_row in enumerate(soup.find("table", class_="dextable").find_all("tr")):
        if idx == 0:
            continue

        _index_children = index_row.find_all("td")

        pokemon_image = _index_children[0].find("a").find("img")["src"]
        _pokemon_link_element = _index_children[1].find("a")
        _pokemon_link = _pokemon_link_element["href"]
        name = _pokemon_link_element.find("u").text
        type_id = MAP_POKEMON_TYPE[_index_children[2].text]
        sleep_type_id = MAP_SLEEP_TYPE_TO_ID[_index_children[3].text]
        specialty = MAP_SPECIALTY_TO_ID[_index_children[4].text]
        pokemon_id = int(pokemon_image.split("/")[4].split(".")[0])

        print(f"Adding pokemon #{pokemon_id} ({name})")

        _pokemon_soup = BeautifulSoup(
            send_requests([f"{POKEMON_URL_PREFIX}{_pokemon_link}"])[0].content,
            "html.parser"
        )

        _tabs = _pokemon_soup.find("main").find_all("table", class_="tab")

        _table_of_evolution_chain = _pokemon_soup.find("table", class_="evochain")
        _evo_chain_is_1st_pokemon = False
        _evo_chain_origin_id = -1
        _evo_chain_conditions = []
        for _evo_chain_row in _table_of_evolution_chain.find_all("tr"):
            for _evo_chain_cell in _evo_chain_row.find_all("td"):
                if _evo_chain_cell.next.name == "table":
                    continue

                if "pkmn" in _evo_chain_cell.get("class", []):
                    _evo_pokemon_id = int(_evo_chain_cell.find("a").find("img")["src"].split("/")[4].split(".")[0])
                    if _evo_chain_origin_id == -1:
                        _evo_chain_origin_id = _evo_pokemon_id
                    else:
                        pokemon_evo_chain[_evo_chain_origin_id][_evo_pokemon_id] = list(set(_evo_chain_conditions))
                        _evo_chain_conditions = []
                else:
                    _evo_chain_conditions.append(_evo_chain_cell.text.replace("  ", " ").strip())

        _tab_of_stats = _tabs[5]
        stats = {}
        for idx_stats, _stats_row in enumerate(_tab_of_stats.find_all("tr")):
            if idx_stats == 0:
                continue

            stat_key = _stats_row.find("td", class_="fooblack").text
            stat_value = _stats_row.find("td", class_="fooinfo").text
            stats[stat_key] = stat_value if ":" in stat_value else int(stat_value)
        stats = transform_stats(stats)

        _rows_of_berry_ingredients = _tabs[6].find_all("tr")
        _row_berry = _rows_of_berry_ingredients[1].find_all("td")
        _berry_img = _row_berry[1].find("a").find("img")
        berry_id = MAP_BERRY[_berry_img["alt"]]
        berry_qty = int(_row_berry[3].text)

        ingredients = {}
        for idx_ingredient, _row_ingredient in enumerate(_rows_of_berry_ingredients[2:]):
            _ingredient_img = _row_ingredient.find_all("td")[1 if idx_ingredient == 0 else 0].find("a").find("img")
            _ingredient_name = _ingredient_img["alt"]
            _ingredient_id = MAP_INGREDIENT_TO_ID[_ingredient_name]

            if idx_ingredient == 0:
                ingredients["fixed"] = _ingredient_id
                continue

            if "random" not in ingredients:
                ingredients["random"] = CUSTOM_RANDOM_INGREDIENT.get(pokemon_id, set())

            ingredients["random"].add(_ingredient_id)

        _main_skill_name, _main_skill_description = _tabs[7].find_all("tr")[1].find_all("td")[:2]
        main_skill = get_main_skill_id(_main_skill_name.text, _main_skill_description.text)

        _table_sleeps = _pokemon_soup.find("table", class_="dextable")
        sleeps = []
        _sleep_1 = {}
        _sleep_2 = {}
        for idx_sleep, _sleep_row in enumerate(_table_sleeps.find_all("tr")):
            idx_ = idx_sleep % 4
            if idx_ == 0:
                continue

            if idx_ == 1:
                for _idx_sleep_cell, _sleep_cell in enumerate(_sleep_row.find_all("td")[:2]):
                    _sleep_cell_img = _sleep_cell.find("img") or BeautifulSoup(
                        f"<{_sleep_cell(text=lambda text: isinstance(text, Comment))[0]}>", "html.parser"
                    ).find("img")

                    if _idx_sleep_cell == 0:
                        _sleep_1["style"] = get_sleep_style_id(pokemon_id, _sleep_cell_img["alt"])
                    elif _idx_sleep_cell == 1:
                        _sleep_2["style"] = get_sleep_style_id(pokemon_id, _sleep_cell_img["alt"])
                continue

            if idx_ == 2:
                for _idx_location_cell, _location_cell in enumerate(_sleep_row.find_all("td")[:2]):
                    _locations = []
                    _location_elements = _location_cell(
                        text=lambda text: isinstance(text, NavigableString) or isinstance(text, Tag)
                    )

                    _location_id = -1
                    for _idx_location, _location_element in enumerate(_location_elements):
                        if _idx_location == 0:
                            continue

                        if _idx_location % 2 == 1:
                            _location_id = MAP_FIELD_TO_ID[_location_element.text]

                        if _idx_location % 2 == 0:
                            title, number = _location_element.text.split(" - From ", 2)[1].split(" ")

                            _locations.append({
                                "id": _location_id,
                                "rank": {
                                    "title": MAP_TITLE_TO_ID[title],
                                    "number": int(number),
                                }
                            })

                    if not _locations and idx_sleep < 4:
                        warnings.warn(
                            f"Pokemon #{pokemon_id} ({name}) does not have location of sleep style - "
                            f"possibly available only through incense"
                        )

                    if _idx_location_cell == 0:
                        _sleep_1["location"] = _locations
                    elif _idx_location_cell == 1:
                        _sleep_2["location"] = _locations

            if idx_ == 3:
                def transform_reward(cell):
                    rewards = [
                        text.text for idx_2, text in
                        enumerate(cell(text=lambda text: isinstance(text, NavigableString))) if idx_2 != 0
                    ]

                    return {
                        "exp": int(next(reward.split(" ")[0] for reward in rewards if reward.endswith("EXP"))),
                        "shards": int(
                            next(reward.split(" ")[0] for reward in rewards if reward.endswith("Dream Shards"))),
                        "candy": int(next(reward.split(" ")[0] for reward in rewards if reward.endswith("Candy"))),
                    }

                for _idx_reward_cell, _reward_cell in enumerate(_sleep_row.find_all("td")[:2]):
                    if _idx_reward_cell == 0:
                        _sleep_1["rewards"] = transform_reward(_reward_cell)
                    elif _idx_reward_cell == 1:
                        _sleep_2["rewards"] = transform_reward(_reward_cell)

                if _sleep_1:
                    sleeps.append(_sleep_1)
                    _sleep_1 = {}
                if _sleep_2:
                    sleeps.append(_sleep_2)
                    _sleep_2 = {}

        if "fixed" not in ingredients and pokemon_id in CUSTOM_FIXED_INGREDIENT:
            ingredients["fixed"] = CUSTOM_FIXED_INGREDIENT[pokemon_id]

        if "random" not in ingredients and pokemon_id in CUSTOM_RANDOM_INGREDIENT:
            ingredients["random"] = CUSTOM_RANDOM_INGREDIENT[pokemon_id]

        if "random" in ingredients:
            # Random should always contain fixed
            ingredients["random"].add(ingredients["fixed"])
        elif "fixed" in ingredients:
            ingredients["random"] = {ingredients["fixed"]}

        pokemon_data.append({
            "id": pokemon_id,
            "name": name,
            "type": type_id,
            "specialty": specialty,
            "sleepType": sleep_type_id,
            "stats": stats,
            "berry": {
                "id": berry_id,
                "quantity": berry_qty
            },
            "ingredients": ingredients,
            "skill": main_skill,
            "sleepStyle": sleeps
        })

    to_json(pokemon_data, "pokemon_data")
    to_json(pokemon_evo_chain, "pokemon_evo_chain")


if __name__ == "__main__":
    main()
