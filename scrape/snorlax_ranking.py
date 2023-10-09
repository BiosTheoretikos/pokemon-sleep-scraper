from _const import *
from _functions import *

PAGE_URL = "https://serebii.net/pokemonsleep/researchareas.shtml"
MAP_URL_PREFIX = "https://serebii.net/pokemonsleep/"


def main():
    snorlax_rank_data = []

    for idx, _map_soup in enumerate(get_soups_of_maps(), start=1):
        map_id = idx
        map_snorlax_rank_data = []
        map_name = _map_soup.find("h1").text

        print(f"Checking map #{map_id} ({map_name})")

        for _possible_rank_table in _map_soup.find_all("table", class_="dextable"):
            _first_table_cell = _possible_rank_table.find_all("td")[0].text
            if _first_table_cell != "Rank":
                continue

            for rank_idx, rank_row in enumerate(_possible_rank_table.find_all("tr")):
                if rank_idx < 1:
                    continue

                _rank_row_data = rank_row.find_all("td")

                _rank_title, _rank_number = _rank_row_data[0].text.split(" ")
                rank = {
                    "title": MAP_TITLE_TO_ID[_rank_title],
                    "number": int(_rank_number),
                }
                energy = int(_rank_row_data[1].text.replace(",", ""))

                map_snorlax_rank_data.append({"rank": rank, "energy": energy})

            snorlax_rank_data.append({"mapId": map_id, "data": map_snorlax_rank_data})

    to_json(snorlax_rank_data, "snorlax_rank")


if __name__ == "__main__":
    main()
