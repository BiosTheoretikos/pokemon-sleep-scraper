import json

# HomeMenuBuiltin
# - Map: HomeMenuScene_HomeMenuView_MapButton
# - Pokedex: HomeMenuScene_HomeMenuView_PokedexButton
# Tutorial
# - Sleep Type: md_tutorial_stories_message_4_1
# - Pokemon Type: md_tutorial_stories_message_9_5
# - Berry: md_tutorial_stories_message_17_2
# - Skill: PokemonNature_Text_1

DIRECTORIES = {
    "Berry": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\Berries",
    "Field": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\Fields",
    "Food": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\CookingFood",
    "MainSkill": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\Skills",
    "PokemonType": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\PokemonType",
    "PokemonName": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\Pokemons",
    "RankTitle": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\SnorlaxRank",
    "SleepType": r"D:\Personal@HDD\Reverse Engineering\PKS\PKS-AR\Texts\SleepType",
}

PREFIXES = {
    "Berry": "md_berries_name_",
    "Field": "md_fields_name_",
    "Food": "md_cooking_foods_name_",
    "MainSkill": {
        "Name": "md_pokemon_main_skills_name_",
        "Description": "md_pokemon_main_skills_desc_",
    },
    "PokemonType": "md_pokemon_types_name_",
    "PokemonName": "md_pokemons_name_",
    "RankTitle": "SnorlaxRank_Main_",
    "SleepType": "SleepType_",
}

FILE_EN = {
    "Berry": "MD_berries_9.bytes.json",
    "Field": "MD_fields_12.bytes.json",
    "Food": "MD_cooking_foods_0.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_2.bytes.json",
    "PokemonType": "MD_pokemon_types_0.bytes.json",
    "PokemonName": "MD_pokemons_0.bytes.json",
    "RankTitle": "SnorlaxRank_Main_1.bytes.json",
    "SleepType": "SleepType_12.bytes.json",
}

FILE_ZH = {
    "Berry": "MD_berries_2.bytes.json",
    "Field": "MD_fields_2.bytes.json",
    "Food": "MD_cooking_foods_2.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_5.bytes.json",
    "PokemonType": "MD_pokemon_types_9.bytes.json",
    "PokemonName": "MD_pokemons_8.bytes.json",
    "RankTitle": "SnorlaxRank_Main_4.bytes.json",
    "SleepType": "SleepType_5.bytes.json",
}

FILE_JP = {
    "Berry": "MD_berries_14.bytes.json",
    "Field": "MD_fields_5.bytes.json",
    "Food": "MD_cooking_foods_4.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_11.bytes.json",
    "PokemonType": "MD_pokemon_types_17.bytes.json",
    "PokemonName": "MD_pokemons_11.bytes.json",
    "RankTitle": "SnorlaxRank_Main_8.bytes.json",
    "SleepType": "SleepType_12.bytes.json",
}

FILE_KR = {
    "Berry": "MD_berries_6.bytes.json",
    "Field": "MD_fields_1.bytes.json",
    "Food": "MD_cooking_foods_6.bytes.json",
    "MainSkill": "MD_pokemon_main_skills_9.bytes.json",
    "PokemonType": "MD_pokemon_types_3.bytes.json",
    "PokemonName": "MD_pokemons_4.bytes.json",
    "RankTitle": "SnorlaxRank_Main_0.bytes.json",
    "SleepType": "SleepType_2.bytes.json",
}

FILE_OF_LOCALE = {
    "en": FILE_EN,
    "zh": FILE_ZH,
    "ja": FILE_JP,
    "kr": FILE_KR
}

UNICODE_REPLACE = [
    # Number
    ("\u000e\u0002\u0006\u0004\u0000촁", " {#1} "),
    ("\u000e\u0002\u0006\u0004\u0001촁", " {#2} "),
    ("\u000e\u0002\u0006\u0004\u0000촂", " {#1} "),
    ("\u000e\u0002\u0006\u0004\u0001촂", " {#2} "),
    # Pokemon type
    ("\u000e\u0003\u0002\u0002촀", " {Element} "),
    # Placeholders
    ("\u0000", ""),
    # Direct replace
    ("\u000e\t\u0000\u0006mmm\u0001", " {?} "),
    ("\u000e\t\f\bmmmm\u0001", " {?} "),
    ("\u000e\t\u0006mmm\u0001", " {?} "),
    ("\u000e\u00010\u0014ingredient\u0016", ""),
    # Remove unwanted string
    ("\u000e\u0001\u001c Shard\f", ""),
    ("촀.", ""),
    ("촀 ", " "),
    ("  ", " "),
    (" .", ""),
    (" 。", ""),
    # next-intl escape
    # https://next-intl-docs.vercel.app/docs/usage/messages#rendering-messages
    ("{", "'{"),
    ("}", "'}"),
]


def values_to_string(locale, values):
    string = "\u0000".join(values).replace("\n", " " if locale == "en" else "")

    for replace_old, replace_new in UNICODE_REPLACE:
        string = string.replace(replace_old, replace_new)

    return string


def fix_string_by_key(key, string):
    if key == "md_pokemon_main_skills_name_1":
        # Charge Strength S (#)
        return f"{string} (#)"

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


def load_string_map_from_data(data, locale, prefix):
    if isinstance(prefix, dict):
        return {key: load_string_map_from_data(data, locale, value) for key, value in prefix.items()}

    data_ret = {}
    for key, values in data["strings"].items():
        if not key.startswith(prefix):
            continue

        data_ret[key.replace(prefix, "")] = fix_string_by_key(key, values_to_string(locale, values))

    return data_ret


def load_string_map(file_path, locale, prefix):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return load_string_map_from_data(data, locale, prefix)


def main():
    for locale, file_path_map in FILE_OF_LOCALE.items():
        print(f"Processing {locale}...")
        data = {
            namespace: load_string_map(rf"{DIRECTORIES[namespace]}\{file_name}", locale, PREFIXES[namespace])
            for namespace, file_name in file_path_map.items()
        }

        with open(f"../data/game-{locale}.json", "w+", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Processed {locale}")


if __name__ == '__main__':
    main()
