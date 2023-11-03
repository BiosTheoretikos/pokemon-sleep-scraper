import os

RENAME_DIR = r"C:\Users\RaenonX\Documents\Projects\PokemonSleep\pokemon-sleep-ui\public\images\dishes\icons"
PREFIX = "cooking_food_"


def main():
    for filename in os.listdir(RENAME_DIR):
        if filename.endswith(".png.png"):
            os.rename(
                rf"{RENAME_DIR}\{filename}",
                rf"{RENAME_DIR}\{filename.replace('.png.png', '.png')}"
            )
            continue

        if len(filename) < 8:
            continue

        file_2nd_half = filename.split(PREFIX, 1)[1]
        item_id = file_2nd_half.split("_", 1)[0].split(".", 1)[0]
        os.rename(
            rf"{RENAME_DIR}\{filename}",
            rf"{RENAME_DIR}\{int(item_id)}.png"
        )


if __name__ == '__main__':
    main()
