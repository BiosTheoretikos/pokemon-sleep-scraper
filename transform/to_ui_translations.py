import json

DIRECTORY = r"C:\Users\RaenonX\Documents\Projects\PokemonSleep\pokemon-sleep-assets\texts"
# Directory from BronzeMaster5000
# DIRECTORY = r"C:\Users\Anwender\Documents\Pokemon Sleep Stuff\TextAll"

PREFIXES = {
    "Berry": "md_berries_name_",
    "Field": "md_fields_name_",
    "Food": "md_cooking_foods_name_",
    "Item": "item_name_",
    "Nature": "md_pokemon_nature_name_",
    "NatureEffect": "PokemonNature_Text_",
    "MainSkill": {
        "Name": "md_pokemon_main_skills_name_",
        "Description": "md_pokemon_main_skills_desc_",
    },
    "MealType": "CookingGenre_Name_",
    "PokemonType": "md_pokemon_types_name_",
    "PokemonName": "md_pokemons_name_",
    "RankTitle": "SnorlaxRank_Main_",
    "SleepFace": "md_sleeping_faces_name_",
    "SleepType": "SleepType_",
    "Specialty": "FormationTag_",
    "SubSkill": {
        "Name": "md_pokemon_rankup_bonus_name_",
        "Description": "md_pokemon_rankup_bonus_desc_",
    },
}

FILE_EN = {
    "Berry": "MD_berries_9.bytes.json",
    "Field": "MD_fields_12.bytes.json",
    "Food": "MD_cooking_foods_0.bytes.json",
    "Item": "MD_item_name_data_17.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_2.bytes.json",
    "MealType": "CookingGenre_11.bytes.json",
    "Nature": "MD_pokemon_nature_15.bytes.json",
    "NatureEffect": "MasterDataModels_GROUP_0.bytes.json",
    "PokemonType": "MD_pokemon_types_0.bytes.json",
    "PokemonName": "MD_pokemons_0.bytes.json",
    "RankTitle": "SnorlaxRank_Main_1.bytes.json",
    "SleepFace": "MD_sleeping_faces.bytes.json",
    "SleepType": "SleepType_12.bytes.json",
    "Specialty": "FormationTag_6.bytes.json",
    "SubSkill": "MD_pokemon_rankup_bonus_12.bytes.json",
}

FILE_ZH = {
    "Berry": "MD_berries_2.bytes.json",
    "Field": "MD_fields_2.bytes.json",
    "Food": "MD_cooking_foods_2.bytes.json",
    "Item": "MD_item_name_data_9.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_5.bytes.json",
    "MealType": "CookingGenre_12.bytes.json",
    "Nature": "MD_pokemon_nature_7.bytes.json",
    "NatureEffect": "MasterDataModels_GROUP_15.bytes.json",
    "PokemonType": "MD_pokemon_types_9.bytes.json",
    "PokemonName": "MD_pokemons_8.bytes.json",
    "RankTitle": "SnorlaxRank_Main_4.bytes.json",
    "SleepFace": "MD_sleeping_faces_14.bytes.json",
    "SleepType": "SleepType_5.bytes.json",
    "Specialty": "FormationTag_13.bytes.json",
    "SubSkill": "MD_pokemon_rankup_bonus_5.bytes.json",
}

FILE_JP = {
    "Berry": "MD_berries_14.bytes.json",
    "Field": "MD_fields_5.bytes.json",
    "Food": "MD_cooking_foods_4.bytes.json",
    "Item": "MD_item_name_data_6.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_11.bytes.json",
    "MealType": "CookingGenre_15.bytes.json",
    "Nature": "MD_pokemon_nature_1.bytes.json",
    "NatureEffect": "MasterDataModels_GROUP_13.bytes.json",
    "PokemonType": "MD_pokemon_types_17.bytes.json",
    "PokemonName": "MD_pokemons_11.bytes.json",
    "RankTitle": "SnorlaxRank_Main_8.bytes.json",
    "SleepFace": "MD_sleeping_faces_9.bytes.json",
    "SleepType": "SleepType_12.bytes.json",
    "Specialty": "FormationTag_15.bytes.json",
    "SubSkill": "MD_pokemon_rankup_bonus_4.bytes.json",
}

FILE_KR = {
    "Berry": "MD_berries_6.bytes.json",
    "Field": "MD_fields_1.bytes.json",
    "Food": "MD_cooking_foods_6.bytes.json",
    "Item": "MD_item_name_data_2.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_9.bytes.json",
    "MealType": "CookingGenre_2.bytes.json",
    "Nature": "MD_pokemon_nature_13.bytes.json",
    "NatureEffect": "MasterDataModels_GROUP_7.bytes.json",
    "PokemonType": "MD_pokemon_types_3.bytes.json",
    "PokemonName": "MD_pokemons_4.bytes.json",
    "RankTitle": "SnorlaxRank_Main_0.bytes.json",
    "SleepFace": "MD_sleeping_faces_10.bytes.json",
    "SleepType": "SleepType_2.bytes.json",
    "Specialty": "FormationTag_1.bytes.json",
    "SubSkill": "MD_pokemon_rankup_bonus_11.bytes.json",
}

FILE_DE = {
    "Berry": "MD_berries_1.bytes.json",
    "Field": "MD_fields_8.bytes.json",
    "Food": "MD_cooking_foods_9.bytes.json",
    "Item": "MD_item_name_data_0.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_0.bytes.json",
    "MealType": "CookingGenre_7.bytes.json",
    "Nature": "MD_pokemon_nature_2.bytes.json",
    "NatureEffect": "MasterDataModels_GROUP.bytes.json",
    "PokemonType": "MD_pokemon_types_2.bytes.json",
    "PokemonName": "MD_pokemons_9.bytes.json",
    "RankTitle": "SnorlaxRank_Main_2.bytes.json",
    "SleepFace": "MD_sleeping_faces_5.bytes.json",
    "SleepType": "SleepType_1.bytes.json",
    "Specialty": "FormationTag_9.bytes.json",
    "SubSkill": {
        "Name": "MD_pokemon_rankup_bonus_6.bytes.json",
        "Description": "MD_pokemon_rankup_bonus_0.bytes.json",
    },
}

FILE_OF_LOCALE = {
    "en": FILE_EN,
    "zh": FILE_ZH,
    "ja": FILE_JP,
    "kr": FILE_KR,
    "de": FILE_DE,
}

UNICODE_REPLACE = {
    # Number
    "\u000e\u0002\u0006\u0004\u0000촁": " {#1} ",
    "\u000e\u0002\u0006\u0004\u0001촁": " {#2} ",
    "\u000e\u0002\u0006\u0004\u0000촂": " {#1} ",
    "\u000e\u0002\u0006\u0004\u0001촂": " {#2} ",
    # Pokemon type
    "\u000e\u0003\u0002\u0002촀": " {Element} ",
    # Placeholders
    "\u0000": "",
    # Direct replace
    "\u000e\t\u0000\u0006mmm\u0001": " {?} ",
    "\u000e\t\f\bmmmm\u0001": " {?} ",
    "\u000e\t\u0006mmm\u0001": " {?} ",
    "\u000e\t \u0006mmm\u0001": " {?} ",
    "\u000e\u00010\u0014ingredient\u0016": "",
    "\u000e\u0006\u001e Zutat\u000e": "",
    # Remove unwanted string
    "\u000e\u0001\u001c Shard\f": "",
    "촀.": "",
    "촀 ": " ",
    "촀": " ",
    "  ": " ",
    " .": "",
    " 。": "",
    "- ": "-",
    # next-intl escape
    # https://next-intl-docs.vercel.app/docs/usage/messages#rendering-messages
    "{": "'{",
    "}": "'}",
    # Direct replace (no next-intl escape)
    # --- For subskill bonus
    "\u000e\u0002\u0001\u0002": "{bonus}",
    "\u000e\u0002\u0003\u0004촁": "{bonus}",
}


def values_to_string(locale, values):
    string = "\u0000".join(values).replace("\n", " " if locale in ("en", "kr", "de") else "")

    for replace_old, replace_new in UNICODE_REPLACE.items():
        string = string.replace(replace_old, replace_new)

    return string


def fix_string_by_key(locale, key, string):
    if key == "md_pokemon_main_skills_name_1":
        # Charge Strength S (#)
        return f"{string} (#)"

    if locale == "ja" and key == "SleepType_0":
        return f"ぐっすり"

    if locale == "ja" and key == "SleepType_1":
        return f"すやすや"

    if locale == "ja" and key == "SleepType_4":
        return f"うとうと"

    if key == "md_pokemon_main_skills_name_5":
        # Charge Strength S (#1 ~ #2)
        return f"{string} (#1 ~ #2)"

    if key == "md_pokemon_main_skills_name_3":
        # Dream Shard Magnet S (#)
        return f"{string} (#)"

    if key == "md_pokemon_main_skills_name_6":
        # Dream Shard Magnet S (#1 ~ #2)
        return f"{string} (#1 ~ #2)"

    return string


def fix_key(key, namespace, prefix):
    key = key.replace(prefix, "")

    if namespace == "SleepFace":
        key = key.split("-")[0]

    return key


def get_value(key, values, namespace, locale):
    value = values_to_string(locale, values)

    if namespace == "SleepFace":
        if "-" not in key:
            # Likely onSnorlax
            return {"Default": value}

        sleep_face_id = key.split("-")[1]

        return {sleep_face_id: value}

    return fix_string_by_key(locale, key, value)


def load_string_map_from_data(data, locale, prefix, namespace):
    if isinstance(prefix, dict):
        return {key: load_string_map_from_data(data, locale, value, namespace) for key, value in prefix.items()}

    data_ret = {}
    for key, values in data["strings"].items():
        if not key.startswith(prefix):
            continue

        # Value goes first because `get_value()` depends on the original key
        value = get_value(key, values, namespace, locale)
        key = fix_key(key, namespace, prefix)
        original_value = data_ret.get(key)

        if isinstance(original_value, dict) and isinstance(value, dict):
            value |= original_value
        elif original_value:
            print(f"Key {key} has value to return ({original_value}), skipped overwriting ({value})")
            continue

        data_ret[key] = value

    return data_ret


def load_string_map(namespace, file_path, locale, prefix):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return load_string_map_from_data(data, locale, prefix, namespace)


def main():
    for locale, file_path_map in FILE_OF_LOCALE.items():
        print(f"Processing {locale}...")
        data = {}
        for namespace, possible_file_name in file_path_map.items():
            if isinstance(possible_file_name, dict):
                data_sub = {}

                # Might want to refactor this to be recursive
                for sub_namespace, file_name in possible_file_name.items():
                    data_sub[sub_namespace] = load_string_map(
                        namespace,
                        rf"{DIRECTORY}\{file_name}",
                        locale,
                        PREFIXES[namespace]
                    )[sub_namespace]

                data[namespace] = data_sub
                continue

            data[namespace] = load_string_map(
                namespace,
                rf"{DIRECTORY}\{possible_file_name}",
                locale,
                PREFIXES[namespace]
            )

        with open(f"export/game-{locale}.json", "w+", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Processed {locale}")


if __name__ == '__main__':
    main()
