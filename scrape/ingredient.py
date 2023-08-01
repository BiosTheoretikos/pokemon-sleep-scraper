from bs4 import BeautifulSoup

from _functions import *

with open("game-en.json", "r", encoding="utf-8") as f:
    game_data = json.load(f)

FOOD_TO_ID = {
    name.replace("“", "").replace("”", ""): food_id
    for food_id, name in game_data["Food"].items()
}

INDEX_URL = "https://www.serebii.net/pokemonsleep/ingredients.shtml"

DISH_URL_PREFIX = "https://www.serebii.net"


def main():
    data_ingredient = []

    req = send_requests([INDEX_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    for idx, index_row in enumerate(soup.find_all("table", class_="dextable")[1].find_all("tr")):
        if idx == 0:
            continue

        _dish_name_element = index_row.find_all("td")[1]
        ingredient_id = FOOD_TO_ID[_dish_name_element.text]

        print(_dish_name_element.text)

        _dish_link = _dish_name_element.find("a")["href"]
        _dish_soup = BeautifulSoup(
            send_requests([f"{DISH_URL_PREFIX}{_dish_link}"])[0].content,
            "html.parser"
        )

        _stats = {}
        _stats_table = _dish_soup.find_all("table", class_="tab")[2]
        for _idx, _row in enumerate(_stats_table.find_all("tr")):
            if _idx == 0:
                continue

            if _idx == 1:
                _stats["price"] = int(_row.find_all("td")[1].text.split(" ")[0])

            if _idx == 2:
                _stats["energy"] = int(_row.find_all("td")[1].text)

        data_ingredient.append({
                                   "id": int(ingredient_id)
                               } | _stats)

    to_json(data_ingredient, "ingredient_data")


if __name__ == '__main__':
    main()
