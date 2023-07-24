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
    "MainSkill": "md_pokemon_main_skills_name_",
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
    "MainSkill": "MD_pokemon_main_skills_3.bytes.json",
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


def load_string_map(file_path, prefix):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        key.replace(prefix, ""): values[0] for key, values in data["strings"].items()
        if key.startswith(prefix)
    }


def main():
    for locale, file_path_map in FILE_OF_LOCALE.items():
        print(f"Processing {locale}...")
        data = {
            namespace: load_string_map(rf"{DIRECTORIES[namespace]}\{file_name}", PREFIXES[namespace])
            for namespace, file_name in file_path_map.items()
        }

        with open(f"../data/game-{locale}.json", "w+", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Processed {locale}")


if __name__ == '__main__':
    main()
