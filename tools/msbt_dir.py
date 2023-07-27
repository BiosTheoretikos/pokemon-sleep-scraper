import os

file_dir = r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\Common"


def main():
    for filename in os.listdir(file_dir):
        if not filename.endswith(".bytes"):
            continue

        source_path = rf"{file_dir}\{filename}"
        output = rf"{file_dir}\{filename}.json"

        print(f"{source_path} -> {output}")

        os.system(f"py msbt.py \"{source_path}\" -x -j \"{output}\"")


if __name__ == '__main__':
    main()
