import warnings
from collections import defaultdict

from bs4 import NavigableString, Tag

from _const import *
from _functions import *

INDEX_URL = "https://www.serebii.net/pokemonsleep/pokemon.shtml"

POKEMON_URL_PREFIX = "https://www.serebii.net/"

with open("data/manual/pokemon/sleep_strings.json", "r", encoding="utf-8") as f:
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

with open("data/manual/pokemon/branch.json") as f:
    pokemon_branches = json.load(f)


def get_sleep_style_id(poke, name):
    if name == "Atop-Belly Sleep":
        return "onSnorlax"

    try:
        return MAP_OF_TO_SLEEP_STYLE_ID[poke][name]
    except KeyError:
        raise RuntimeError(f"{poke} ({name})")


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


def to_rank_object(rank_text):
    title, number = rank_text.split(" ")

    return {
        "title": MAP_TITLE_TO_ID[title],
        "number": int(number),
    }


def get_pokemon_to_sleep_style_mapping():
    ret = defaultdict(lambda: defaultdict(list))

    for _map_soup in get_soups_of_maps():
        map_name = _map_soup.find("h1").text

        for idx, _sleep_style_row in enumerate(_map_soup.find_all("table", class_="dextable")[-1].find_all("tr")):
            if idx == 0:
                continue

            _rank, _, _styles = _sleep_style_row.find_all("td")

            _rank_text = _rank.text
            _styles_text = _styles.get_text(separator="\n", strip=True)

            if not _styles_text:
                continue

            _styles_list = _styles_text.replace("\n-", " -").split("\n")

            rank_obj = to_rank_object(_rank_text)

            for _style in _styles_list:
                if " - " not in _style:
                    # Sleep style string could be malformed
                    # Example:
                    # G5 got "Ditto -" in https://www.serebii.net/pokemonsleep/locations/snowdroptundra.shtml
                    continue

                _pokemon_name, _style_name = _style.split(" - ", 2)

                ret[_pokemon_name][_style_name].append({
                    "id": MAP_FIELD_TO_ID[map_name],
                    "rank": rank_obj
                })

    return ret


def get_pokemon_data(tabs, start_idx):
    _tab_of_stats = tabs[start_idx + 1]
    stats = {}
    for idx_stats, _stats_row in enumerate(_tab_of_stats.find_all("tr")):
        if idx_stats == 0:
            continue

        stat_key = _stats_row.find("td", class_="fooblack").text
        stat_value = _stats_row.find("td", class_="fooinfo").text
        stats[stat_key] = stat_value if ":" in stat_value else int(stat_value)
    stats = transform_stats(stats)

    _rows_of_berry_ingredients = tabs[start_idx + 2].find_all("tr")
    _row_berry = _rows_of_berry_ingredients[1].find_all("td")
    _berry_img = _row_berry[1].find("a").find("img")
    berry_id = MAP_BERRY[_berry_img["alt"]]
    berry_qty = int(_row_berry[3].text)

    _main_skill_name, _main_skill_description = tabs[start_idx + 3].find_all("tr")[1].find_all("td")[:2]
    main_skill = get_main_skill_id(_main_skill_name.text, _main_skill_description.text)

    return stats, berry_id, berry_qty, main_skill


def main():
    pokemon_data = []

    req = send_requests([INDEX_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    print("Preparing pokemon to sleep style mapping")
    sleep_style_info_from_map = get_pokemon_to_sleep_style_mapping()

    for idx, index_row in enumerate(soup.find("table", class_="dextable").find_all("tr")):
        if idx == 0:
            continue

        _index_children = index_row.find_all("td")

        pokemon_image = _index_children[0].find("a").find("img")["src"]
        pokemon_id = int(pokemon_image.split("/")[4].split(".")[0])
        _pokemon_link_element = _index_children[1].find("a")
        _pokemon_link = _pokemon_link_element["href"]
        pokemon_name = _pokemon_link_element.find("u").text

        print(f"Adding Pokemon #{pokemon_id} ({pokemon_name})")

        type_id = MAP_POKEMON_TYPE[_index_children[2].text]
        sleep_type_id = MAP_SLEEP_TYPE_TO_ID[_index_children[3].text]
        specialty = MAP_SPECIALTY_TO_ID[_index_children[4].text]

        _pokemon_soup = BeautifulSoup(
            send_requests([f"{POKEMON_URL_PREFIX}{_pokemon_link}"])[0].content,
            "html.parser"
        )

        _tabs = _pokemon_soup.find("main").find_all("table", class_="tab")

        stats, berry_id, berry_qty, main_skill = get_pokemon_data(_tabs, 4)

        _table_sleeps = _pokemon_soup.find("table", class_="dextable")
        sleeps = []
        _sleep_style_name_1 = None
        _sleep_style_name_2 = None
        _sleep_1 = {}
        _sleep_2 = {}
        for _idx_sleep_row, _sleep_row in enumerate(_table_sleeps.find_all("tr")):
            _idx_sleep_row_of_section = _idx_sleep_row % 4
            if _idx_sleep_row_of_section == 0:
                for _idx_sleep_title, _sleep_title in enumerate(_sleep_row.find_all("td")[:2]):
                    if _idx_sleep_title == 0:
                        _sleep_style_name_1 = _sleep_title.text
                        _sleep_1["style"] = get_sleep_style_id(pokemon_id, _sleep_style_name_1)
                    elif _idx_sleep_title == 1:
                        _sleep_style_name_2 = _sleep_title.text
                        _sleep_2["style"] = get_sleep_style_id(pokemon_id, _sleep_style_name_2)
                continue

            if _idx_sleep_row_of_section == 1:
                continue

            if _idx_sleep_row_of_section == 2:
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
                            # Had issue with unknown rank, rendering "Greengrass Isle -"
                            # https://www.serebii.net//pokemonsleep/pokemon/clefairy.shtml
                            _location_rank_info = _location_element.text.split(" - From ", 2)
                            if len(_location_rank_info) < 2:
                                continue

                            _locations.append({
                                "id": _location_id,
                                "rank": to_rank_object(_location_rank_info[1])
                            })

                    if not _locations:
                        lacking_sleep_style = _idx_sleep_row // 4 * 2 + 1

                        if _idx_location_cell == 0:
                            _locations = sleep_style_info_from_map[pokemon_name][_sleep_style_name_1]
                        elif _idx_location_cell == 1:
                            _locations = sleep_style_info_from_map[pokemon_name][_sleep_style_name_2]

                        warnings.warn(
                            f"Pokemon #{pokemon_id} ({pokemon_name}) does not have location of sleep style "
                            f"#{lacking_sleep_style} or #{lacking_sleep_style + 1} - "
                            "possibly available only through incense"
                        )

                    if _idx_location_cell == 0:
                        _sleep_1["location"] = _locations
                    elif _idx_location_cell == 1:
                        _sleep_2["location"] = _locations

            if _idx_sleep_row_of_section == 3:
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

        pokemon_data.append({
            "id": pokemon_id,
            "name": pokemon_name,
            "type": type_id,
            "specialty": specialty,
            "sleepType": sleep_type_id,
            "stats": stats,
            "berry": {
                "id": berry_id,
                "quantity": berry_qty
            },
            "skill": main_skill,
            "sleepStyle": sleeps
        })

        for branch_idx, pokemon_id_branch in enumerate(pokemon_branches.get(str(pokemon_id), []), start=1):
            print(f"Found branch data of #{pokemon_id} ({pokemon_name}) - #{pokemon_id_branch}")
            stats, berry_id, berry_qty, main_skill = get_pokemon_data(_tabs, 4 + branch_idx * 4)

            pokemon_data.append({
                "id": pokemon_id_branch,
                "name": pokemon_name,
                "type": type_id,
                "specialty": specialty,
                "sleepType": sleep_type_id,
                "stats": stats,
                "berry": {
                    "id": berry_id,
                    "quantity": berry_qty
                },
                "skill": main_skill,
                "sleepStyle": sleeps
            })

    to_json(pokemon_data, "pokemon_data")


if __name__ == "__main__":
    main()
