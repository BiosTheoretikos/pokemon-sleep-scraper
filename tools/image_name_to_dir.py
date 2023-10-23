import glob
import shutil
from pathlib import Path

IMAGE_DIR = r"C:\Users\RaenonX\Downloads\A"

IMAGE_DIR_EXPORT = r"C:\Users\RaenonX\Documents\Projects\PokemonSleep\pokemon-sleep-ui\public\images\sleep"


def main():
    dir_3 = rf"{IMAGE_DIR_EXPORT}\3"
    dir_3_shiny = rf"{IMAGE_DIR_EXPORT}\3\shiny"
    dir_4 = rf"{IMAGE_DIR_EXPORT}\onSnorlax"
    dir_4_shiny = rf"{IMAGE_DIR_EXPORT}\onSnorlax\shiny"
    dir_8 = rf"{IMAGE_DIR_EXPORT}\8"
    dir_8_shiny = rf"{IMAGE_DIR_EXPORT}\8\shiny"

    Path(IMAGE_DIR_EXPORT).mkdir(exist_ok=True)
    Path(dir_3).mkdir(exist_ok=True)
    Path(dir_3_shiny).mkdir(exist_ok=True)
    Path(dir_4).mkdir(exist_ok=True)
    Path(dir_4_shiny).mkdir(exist_ok=True)
    Path(dir_8).mkdir(exist_ok=True)
    Path(dir_8_shiny).mkdir(exist_ok=True)

    for file_path in glob.glob(rf"{IMAGE_DIR}\*.png"):
        file_name = file_path.split("\\")[-1]

        pokemon_id = file_name.split("_")[1]
        file_name_new = f"{pokemon_id}.png"

        if file_name.endswith("rare.png"):
            shutil.copy2(file_path, rf"{dir_3}\{file_name_new}")
            print(rf"{file_path} => {dir_3}\{file_name_new}")
            continue

        if file_name.endswith("rare_shiny.png"):
            shutil.copy2(file_path, rf"{dir_3_shiny}\{file_name_new}")
            print(rf"{file_path} => {dir_3_shiny}\{file_name_new}")
            continue

        if file_name.endswith("normal_on_snorlax.png"):
            shutil.copy2(file_path, rf"{dir_4}\{file_name_new}")
            print(rf"{file_path} => {dir_4}\{file_name_new}")
            continue

        if file_name.endswith("normal_on_snorlax_shiny.png"):
            shutil.copy2(file_path, rf"{dir_4_shiny}\{file_name_new}")
            print(rf"{file_path} => {dir_4_shiny}\{file_name_new}")
            continue

        if file_name.endswith("rare_on_snorlax.png"):
            shutil.copy2(file_path, rf"{dir_4}\{file_name_new}")
            print(rf"{file_path} => {dir_4}\{file_name_new}")
            continue

        if file_name.endswith("rare_on_snorlax_shiny.png"):
            shutil.copy2(file_path, rf"{dir_4_shiny}\{file_name_new}")
            print(rf"{file_path} => {dir_4_shiny}\{file_name_new}")
            continue

        if file_name.endswith("sleep_8.png"):
            shutil.copy2(file_path, rf"{dir_4}\{file_name_new}")
            print(rf"{file_path} => {dir_4}\{file_name_new}")
            continue

        if file_name.endswith("sleep_8_shiny.png"):
            shutil.copy2(file_path, rf"{dir_4_shiny}\{file_name_new}")
            print(rf"{file_path} => {dir_4_shiny}\{file_name_new}")
            continue

        print(f"Unhandled file name: {file_name}")
        exit(1)


if __name__ == "__main__":
    main()
