import json
import os
from collections import defaultdict

import grequests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

INDEX_URL = "https://www.serebii.net/pokemonsleep/pokemon.shtml"

POKEMON_URL_PREFIX = "https://www.serebii.net/pokemonsleep/"

# Confirmed in text asset
MAP_BERRY = {
    "Belue Berry": 17,
    "Bluk Berry": 14,
    "Cheri Berry": 7,
    "Chesto Berry": 8,
    "Durin Berry": 5,
    "Figy Berry": 9,
    "Grepa Berry": 4,
    "Leppa Berry": 2,
    "Lum Berry": 12,
    "Mago Berry": 11,
    "Oran Berry": 3,
    "Pamtre Berry": 10,
    "Pecha Berry": 18,
    "Persim Berry": 1,
    "Rawst Berry": 6,
    "Sitrus Berry": 13,
    "Wiki Berry": 16,
    "Yache Berry": 15,
}

# Confirmed in text asset
MAP_TYPE = {
    "Normal": 1,
    "Fire": 2,
    "Water": 3,
    "Electric": 4,
    "Grass": 5,
    "Ice": 6,
    "Fighting": 7,
    "Poison": 8,
    "Ground": 9,
    "Flying": 10,
    "Psychic": 11,
    "Bug": 12,
    "Rock": 13,
    "Ghost": 14,
    "Dragon": 15,
    "Dark": 16,
    "Steel": 17,
    "Fairy": 18,
}

MAP_KEYWORD_TO_SLEEP_TYPE = {
    "drowse": "drowse",
    "sleep": "normal",
    "extra": "unreleased_1",
    "drowsy": "unreleased_2",
}

# Confirmed in text asset
MAP_SKILL_NAME_TO_ID = {
    "Charge Strength M": 2,
    "Energizing Cheer S": 4,
    "Charge Energy S": 7,
    "Energy for Everyone S": 8,
    "Extra Helpful S": 9,
    "Ingredient Magnet S": 10,
    "Cooking Power-Up S": 11,
    "Type Boost S": 12,
    "Metronome": 13
}

# Confirmed in text asset
MAP_SLEEP_TYPE_TO_ID = {
    "Balanced": 99,
    "Dozing": 4,
    "Snoozing": 1,
    "Slumbering": 0,
}

# Confirmed in text asset
MAP_INGREDIENT_TO_ID = {
    "Large Leek": 1,
    "Tasty Mushroom": 2,
    "Fancy Egg": 3,
    "Soft Potato": 4,
    "Fancy Apple": 5,
    "Fiery Herb": 6,
    "Bean Sausage": 7,
    "Moomoo Milk": 8,
    "Honey": 9,
    "Pure Oil": 10,
    "Warming Ginger": 11,
    "Snoozy Tomato": 12,
    "Soothing Cacao": 13,
    "Slowpoke Tail": 14,
    "Greengrass Soybeans": 15
}

# Confirmed in text asset
MAP_FIELD_TO_ID = {
    "Greengrass Isle": 1,
    "Cyan Beach": 2,
    "Taupe Hollow": 3,
    "Snowdrop Tundra": 4,
    "Carmine Volcano": 6,
    "Lapis Lakeside": 7,
}

# Confirm in text asset (Snorlax Rank Main)
MAP_TITLE_TO_ID = {
    "Basic": 1,
    "Great": 2,
    "Ultra": 3,
    "Master": 4
}


with open("transformed/sleep_strings.json", "r", encoding="utf-8") as f:
    MAP_OF_TO_SLEEP_STYLE_ID = {}
    for key, value in json.load(f).items():
        if key == "onSnorlax":
            continue

        pokemon_id, style_type = key.split("-")
        pokemon_id = int(pokemon_id)
        style_type = int(style_type)

        if pokemon_id not in MAP_OF_TO_SLEEP_STYLE_ID:
            MAP_OF_TO_SLEEP_STYLE_ID[pokemon_id] = {}

        MAP_OF_TO_SLEEP_STYLE_ID[pokemon_id][value] = style_type


def get_sleep_style_id(poke, name):
    if name == "Atop-Belly Sleep":
        return "onSnorlax"

    return MAP_OF_TO_SLEEP_STYLE_ID[poke][name]


def send_requests(urls):
    reqs = [grequests.get(url) for url in urls]

    return grequests.map(reqs, size=10)


def download_to_images(urls, output_dir):
    for file_name, response in zip(urls.keys(), send_requests(urls.values())):
        with open(os.path.join(output_dir, f"{file_name}.png"), "w+") as f:
            f.write(response.content)


def to_json(data, filename):
    with open(f"data/{filename}.json", "w+") as f:
        json.dump(data, f, indent=4)


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
    pokemon_data = {}
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
        type_id = MAP_TYPE[_index_children[2].text]
        sleep_type_id = MAP_SLEEP_TYPE_TO_ID[_index_children[3].text]
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

            value = _stats_row.find("td", class_="fooinfo").text
            stats[_stats_row.find("td", class_="fooblack").text] = value if ":" in value else int(value)
        stats = transform_stats(stats)

        _rows_of_berry_ingredients = _tabs[6].find_all("tr")
        _row_berry = _rows_of_berry_ingredients[1].find_all("td")
        _berry_img = _row_berry[1].find("a").find("img")
        berry_id = MAP_BERRY[_berry_img["alt"]]
        berry_qty = int(_row_berry[3].text)

        ingredients = []
        for idx_ingredient, _row_ingredient in enumerate(_rows_of_berry_ingredients[2:]):
            _ingredient_img = _row_ingredient.find_all("td")[1 if idx_ingredient == 0 else 0].find("a").find("img")
            _ingredient_name = _ingredient_img["alt"]

            ingredients.append(MAP_INGREDIENT_TO_ID[_ingredient_name])

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

        pokemon_data[pokemon_id] = {
            "id": pokemon_id,
            "name": name,
            "type": type_id,
            "sleepType": sleep_type_id,
            "stats": stats,
            "berry": {
                "id": berry_id,
                "quantity": berry_qty
            },
            "ingredients": ingredients,
            "skill": main_skill,
            "sleepStyle": sleeps
        }

    to_json(pokemon_data, "pokemon_data")
    to_json(pokemon_evo_chain, "pokemon_evo_chain")


if __name__ == "__main__":
    main()
