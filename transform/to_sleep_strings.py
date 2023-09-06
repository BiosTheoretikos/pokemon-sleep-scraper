import json

DIRECTORY = r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\TextAll"
# Directory from BronzeMaster5000
# DIRECTORY = r"C:\Users\Anwender\Documents\Pokemon Sleep Stuff\TextAll"


FILE_NAME = "MD_sleeping_faces.bytes.json"


def main():
    data_export = {}
    with open(f"{DIRECTORY}/{FILE_NAME}", "r", encoding="utf-8") as f:
        data = json.load(f)

        for key, values in data["strings"].items():
            data_export[key.replace("md_sleeping_faces_name_", "")] = values[0]

    with open("transformed/sleep_strings.json", "w+", encoding="utf-8", newline="\n") as f_export:
        json.dump(data_export, f_export, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
