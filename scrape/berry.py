from _functions import *

with open("data/transformed/game-en.json", "r", encoding="utf-8") as f:
    game_data = json.load(f)

ITEM_TO_ID = {
    name.replace("“", "").replace("”", ""): food_id
    for food_id, name in game_data["Berry"].items()
}

INDEX_URL = "https://www.serebii.net/pokemonsleep/ingredients.shtml"

DISH_URL_PREFIX = "https://www.serebii.net"


def main():
    data_berry = []

    req = send_requests([INDEX_URL])[0]
    soup = BeautifulSoup(req.content, "html.parser")

    for idx, index_row in enumerate(soup.find_all("table", class_="dextable")[0].find_all("tr")):
        if idx == 0:
            continue

        _name_element = index_row.find_all("td")[1]
        item_id = ITEM_TO_ID[_name_element.text]

        print(_name_element.text)

        _index_link = _name_element.find("a")["href"]
        _item_soup = BeautifulSoup(
            send_requests([f"{DISH_URL_PREFIX}{_index_link}"])[0].content,
            "html.parser"
        )

        _energy_data_list = []
        _energy_table = _item_soup.find("table", class_="dextable")
        for _idx_energy, _energy_row in enumerate(_energy_table.find_all("tr")):
            if _idx_energy == 0:
                continue

            _energy_data = _energy_row.find_all("td")
            _poke_lv = int(_energy_data[0].text.split(" ")[1])
            _energy = int(_energy_data[1].text.split(" ")[0])

            _energy_data_list.append({
                "lv": _poke_lv,
                "energy": _energy,
            })

        data_berry.append({
            "id": int(item_id),
            "energy": _energy_data_list
        })

    to_json(data_berry, "berry_data")


if __name__ == '__main__':
    main()
