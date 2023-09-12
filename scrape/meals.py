from bs4 import BeautifulSoup

from _functions import *

with open("export/game-en.json", "r", encoding="utf-8") as f:
    game_data = json.load(f)

FOOD_TO_ID = {
    name.replace("“", "").replace("”", "").replace("’", "'"): food_id
    for food_id, name in game_data["Food"].items()
}

INDEX_URL = "https://www.serebii.net/pokemonsleep/dishes.shtml"

DISH_URL_PREFIX = "https://www.serebii.net"


# _meal_idx confirmed in CookingGenre text asset


def main():
    meal_data = []

    req = send_requests([INDEX_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    _meal_tables = soup.find_all("table", class_="dextable")[1:4]

    for _meal_idx, _meal_table in enumerate(_meal_tables, start=1):
        for idx, index_row in enumerate(_meal_table.find_all("tr")):
            if idx == 0:
                continue

            _dish_name_element = index_row.find_all("td")[1]
            dish_id = FOOD_TO_ID[_dish_name_element.text]

            print(_dish_name_element.text)

            _dish_link = _dish_name_element.find("a")["href"]
            _dish_soup = BeautifulSoup(
                send_requests([f"{DISH_URL_PREFIX}{_dish_link}"])[0].content,
                "html.parser"
            )

            _dish_tables = _dish_soup.find_all("table", class_="dextable")
            _dish_ingredient_table = _dish_tables[0]
            _dish_stats_table = _dish_tables[1]

            ingredients = []
            for _idx_ingredient, _ingredient_row in enumerate(_dish_ingredient_table.find_all("tr")):
                if _idx_ingredient == 0:
                    continue

                _ingredient_data = _ingredient_row.find_all("td")
                _ingredient_name = _ingredient_data[1].text

                if not _ingredient_name:
                    continue

                _ingredient_quantity = int(_ingredient_data[2].text)

                ingredients.append({
                    "id": int(FOOD_TO_ID[_ingredient_name]),
                    "quantity": _ingredient_quantity
                })

            levels = []
            for _idx_stats, _stats_row in enumerate(_dish_stats_table.find_all("tr")):
                if _idx_stats == 0:
                    continue

                _stats_data = _stats_row.find_all("td")
                _stats_exp = int(_stats_data[1].text.replace(",", ""))
                _stats_energy = int(_stats_data[2].text)
                levels.append({
                    "lv": _idx_stats,
                    "exp": _stats_exp,
                    "energy": _stats_energy
                })

            meal_data.append({
                "id": int(dish_id),
                "type": _meal_idx,
                "ingredients": ingredients,
                "levels": levels,
            })

    to_json(meal_data, "meal_data")


if __name__ == '__main__':
    main()
