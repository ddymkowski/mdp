import pytest
import polars as pl
from polars import DataType

from mdp.service.type_agnostic import get_type_agnostic_metrics


@pytest.fixture
def test_data() -> dict[str, list[int | None]]:
    return {
        "col_with_nulls": [1, None, 3, None, 5],
        "col_without_nulls": [1, 2, 3, 4, 5],
    }


@pytest.fixture
def test_dataframe(test_data: dict[str, type[DataType]]) -> pl.DataFrame:
    schema = {
        "col_with_nulls": pl.Int64,
        "col_without_nulls": pl.Int64,
    }
    return pl.DataFrame(data=test_data, schema=schema)


@pytest.mark.parametrize(
    "column_name, expected_null_count",
    [
        ("col_with_nulls", 2),
        ("col_without_nulls", 0),
    ],
)
def test_type_agnostic_profile(
    test_dataframe: pl.DataFrame, column_name: str, expected_null_count: int
) -> None:
    profile = get_type_agnostic_metrics(test_dataframe, column_name)

    assert profile.nulls_count == expected_null_count
