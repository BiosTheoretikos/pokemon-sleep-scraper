from typing import Callable

from pandas import DataFrame


def get_string_key_id_extractor(prefix: str) -> Callable[[str], int]:
    def extractor(key: str) -> int:
        if not key.startswith(prefix):
            raise RuntimeError(f"Key `{key}` must start with `{prefix}`")

        id_in_key = key.split(prefix)[1]
        try:
            return int(id_in_key)
        except ValueError as error:
            raise RuntimeError(
                f"Error occurred during ID extraction from ID in key `{id_in_key}` of key `{key}"
            ) from error

    return extractor


def get_ids_from_df_column_name(df: DataFrame, key_prefix: str) -> list[int]:
    extract_id = get_string_key_id_extractor(key_prefix)

    return [
        extract_id(col_name)
        for col_name in df.columns
        if col_name.startswith(key_prefix)
    ]
