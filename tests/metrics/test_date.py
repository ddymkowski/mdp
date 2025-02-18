from datetime import date, datetime, UTC

import polars as pl
from polars import DataType
from polars.datatypes import Date, Datetime
import pytest

from mdp.models.date_or_datetime import DateOrDateTimeProfile
from mdp.service.date_or_datetime import get_date_or_datetime_metrics


@pytest.fixture
def date_schema() -> dict[str, DataType | type[DataType]]:
    return {
        "date_col": Date,
        "datetime_col": Datetime(time_zone="UTC"),
        "null_date_col": Date,
        "null_datetime_col": Datetime,
    }


@pytest.fixture
def date_data() -> dict[str, list[None | date | datetime]]:
    return {
        "date_col": [
            date(2023, 1, 1),
            date(2023, 12, 31),
            None,
            date(2023, 6, 15),
            date(2023, 3, 1),
        ],
        "datetime_col": [
            datetime(2023, 1, 1, 10, 0, 0),
            datetime(2023, 12, 31, 23, 59, 59),
            None,
            datetime(2023, 6, 15, 12, 30, 45),
            datetime(2023, 3, 1, 8, 15, 0),
        ],
        "null_date_col": [None, None, None, None, None],
        "null_datetime_col": [None, None, None, None, None],
    }


@pytest.fixture
def date_test_data(
    date_data: dict[str, list[str | None]],
    date_schema: dict[str, pl.datatypes.DataTypeClass],
) -> pl.DataFrame:
    return pl.DataFrame(data=date_data, schema=date_schema)


@pytest.mark.parametrize(
    "column_name, expected_profile",
    [
        (
            "date_col",
            DateOrDateTimeProfile(
                nulls_count=1, min=date(2023, 1, 1), max=date(2023, 12, 31)
            ),
        ),
        (
            "datetime_col",
            DateOrDateTimeProfile(
                nulls_count=1,
                min=datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC),
                max=datetime(2023, 12, 31, 23, 59, 59, tzinfo=UTC),
            ),
        ),
        ("null_date_col", DateOrDateTimeProfile(nulls_count=5, min=None, max=None)),
        ("null_datetime_col", DateOrDateTimeProfile(nulls_count=5, min=None, max=None)),
    ],
)
def test_date_profile(
    date_test_data: pl.DataFrame,
    column_name: str,
    expected_profile: DateOrDateTimeProfile,
) -> None:
    profile = get_date_or_datetime_metrics(date_test_data, column_name)
    assert profile == expected_profile
