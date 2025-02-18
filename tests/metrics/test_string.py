import polars
from polars.datatypes import String, Categorical
import pytest

from mdp.models._string import StringProfile
from mdp.service import get_string_metrics


@pytest.fixture
def string_schema() -> dict[str, polars.datatypes.DataTypeClass]:
    return {
        "string_col": String,
        "categorical_col": Categorical,
        "null_string_col": String,
        "null_categorical_col": Categorical,
    }


@pytest.fixture
def string_data() -> dict[str, list[str | None]]:
    return {
        "string_col": ["Hello", "World", None, "", " "],
        "categorical_col": [
            "Category10",
            "Category2",
            "Category Extended",
            "Category1",
            None,
        ],
        "null_string_col": [None, None, None, None, None],
        "null_categorical_col": [None, None, None, None, None],
    }


@pytest.fixture
def string_test_data(
    string_data: dict[str, list[str | None]],
    string_schema: dict[str, polars.datatypes.DataTypeClass],
) -> polars.DataFrame:
    return polars.DataFrame(data=string_data, schema=string_schema)


@pytest.mark.parametrize(
    "column_name, expected_profile",
    [
        (
            "string_col",
            StringProfile(
                nulls_count=1,
                min_length=0,
                max_length=5,
                avg_length=2.75,
                median_length=3.0,
                min_token_count=1,
                max_token_count=2,
                avg_token_count=1.25,
                median_token_count=1,
                empty_or_whitespace_count=2,
            ),
        ),
        (
            "categorical_col",
            StringProfile(
                nulls_count=1,
                min_length=9,
                max_length=17,
                avg_length=11.25,
                median_length=9.5,
                min_token_count=1,
                max_token_count=2,
                avg_token_count=1.25,
                median_token_count=1,
                empty_or_whitespace_count=0,
            ),
        ),
        (
            "null_string_col",
            StringProfile(
                nulls_count=5,
                min_length=None,
                max_length=None,
                avg_length=None,
                median_length=None,
                min_token_count=None,
                max_token_count=None,
                avg_token_count=None,
                median_token_count=None,
                empty_or_whitespace_count=0,
            ),
        ),
        (
            "null_categorical_col",
            StringProfile(
                nulls_count=5,
                min_length=None,
                max_length=None,
                avg_length=None,
                median_length=None,
                min_token_count=None,
                max_token_count=None,
                avg_token_count=None,
                median_token_count=None,
                empty_or_whitespace_count=0,
            ),
        ),
    ],
)
def test_string_profile(
    string_test_data: polars.DataFrame,
    column_name: str,
    expected_profile: StringProfile,
) -> None:
    profile = get_string_metrics(string_test_data, column_name)
    assert profile == expected_profile
