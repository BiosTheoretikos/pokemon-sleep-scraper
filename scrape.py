import datetime
import subprocess
import sys

SCRIPTS_SCRAPER = [
    "scrape_legacy/mainskill.py",
    "scrape_legacy/meals.py",
    "scrape_legacy/pokemon_data.py",
]

SCRIPTS_UPDATE = [
    "controller/put_mainskill_data.py",
    "controller/put_meal_data.py",
    "controller/put_pokemon_data.py",
]

log_file_name = f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d-%H%M%S')}.log"


def run_script(script_type, script_path):
    with open(log_file_name, "ab+") as f:
        f.write(f"--- {script_type}: {script_path}\n".encode("utf-8"))
        process = subprocess.Popen(["py", script_path], stdout=subprocess.PIPE)
        for c in iter(lambda: process.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
            f.write(c)
            f.flush()

        process.wait()
        exit_code = process.returncode
        if exit_code:
            print(f"Exit code non-0 for {script_type} - {script_path} ({exit_code})", file=sys.stderr)
            sys.exit(exit_code)


def main():
    for scraper in SCRIPTS_SCRAPER:
        run_script("Scrape", scraper)

    for update in SCRIPTS_UPDATE:
        run_script("Update", update)


if __name__ == "__main__":
    main()
