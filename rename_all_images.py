import os

rename_dir = r"D:\Personal@HDD\Reverse Engineering\PKS\Picked\candy"


def main():
    for filename in os.listdir(rename_dir):
        if filename.endswith(".png.png"):
            os.rename(
                rf"{rename_dir}\{filename}",
                rf"{rename_dir}\{filename.replace('.png.png', '.png')}"
            )
            continue

        if len(filename) < 8:
            continue

        file_2nd_half = filename.split("candy_", 1)[1]
        pokemon_id = file_2nd_half.split("_", 1)[0].split(".", 1)[0]
        os.rename(
            rf"{rename_dir}\{filename}",
            rf"{rename_dir}\{int(pokemon_id)}.png"
        )


if __name__ == '__main__':
    main()
