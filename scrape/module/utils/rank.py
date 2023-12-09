from pandas import Series


def to_rank_object(row: Series) -> dict[str, int]:
    return {
        "title": row["main_rank"],
        "number": row["sub_rank"],
    }
