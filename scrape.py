import subprocess
import sys
from datetime import datetime

SCRIPTS_SCRAPER = [
    "scrape/berry.py",
    "scrape/ingredient.py",
    "scrape/meals.py",
    "scrape/pokemon_by_incense.py",
    "scrape/pokemon_data_and_evo_chain.py",
    "scrape/snorlax.py",
    "scrape/subskill.py",
]

SCRIPTS_UPDATE = [
    "controller/put_berry_data.py",
    "controller/put_ingredient_data.py",
    "controller/put_map_data.py",
    "controller/put_meal_data.py",
    "controller/put_pokemon_data.py",
    "controller/put_snorlax_data.py",
    "controller/put_subskill_data.py",
    "controller/put_evolution_chain_data.py",
    "controller/put_ingredient_chain_data.py",
]


log_file_name = f"{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.log"


def run_script(script_type, script_path):
    with open(log_file_name, "ab+") as f:
        f.write(f"--- {script_type}: {script_path}\n".encode("utf-8"))
        process = subprocess.Popen(["py", script_path], stdout=subprocess.PIPE)
        for c in iter(lambda: process.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
            f.write(c)
            f.flush()


def main():
    for scraper in SCRIPTS_SCRAPER:
        run_script("Scrape", scraper)

    for update in SCRIPTS_UPDATE:
        run_script("Update", update)


if __name__ == "__main__":
    main()
