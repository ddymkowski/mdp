from dataclasses import asdict

import polars
from polars.datatypes import (
    Float32,
    Float64,
    Int8,
    Int16,
    Int32,
    Int64,
    Int128,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
)
import pytest

from plmdp.models.numeric import NumericProfile
from plmdp.service import get_numeric_metrics


@pytest.fixture
def numeric_schema() -> dict[str, polars.datatypes.DataTypeClass]:
    return {
        "float32_col": Float32,
        "float64_col": Float64,
        "int8_col": Int8,
        "int16_col": Int16,
        "int32_col": Int32,
        "int64_col": Int64,
        "int128_col": Int128,
        "uint8_col": UInt8,
        "uint16_col": UInt16,
        "uint32_col": UInt32,
        "uint64_col": UInt64,
    }


@pytest.fixture
def numeric_data() -> dict[str, list[int | float | None]]:
    return {
        "float32_col": [1.1, 2.2, 3.3, None, 4.4],
        "float64_col": [1.1, 2.2, 3.3, None, 4.4],
        "int8_col": [1, 2, 3, None, 4],
        "int16_col": [1, 2, 3, None, 4],
        "int32_col": [1, 2, 3, None, 4],
        "int64_col": [1, 2, 3, None, 4],
        "int128_col": [1, 2, 3, None, 4],
        "uint8_col": [1, 2, 3, None, 4],
        "uint16_col": [1, 2, 3, None, 4],
        "uint32_col": [1, 2, 3, None, 4],
        "uint64_col": [1, 2, 3, None, 4],
    }


@pytest.fixture
def numeric_test_data(
    numeric_data: dict[str, list[int | float | None]],
    numeric_schema: dict[str, polars.datatypes.DataTypeClass],
) -> polars.DataFrame:
    return polars.DataFrame(data=numeric_data, schema=numeric_schema)


@pytest.mark.parametrize(
    "column_name, expected_profile",
    [
        (
            "float32_col",
            NumericProfile(
                nulls_count=1,
                mean=2.75,
                median=2.75,
                std=1.42,
                min=1.1,
                max=4.4,
                percentile25=2.2,
                percentile50=3.3,
                percentile75=3.3,
            ),
        ),
        (
            "float64_col",
            NumericProfile(
                nulls_count=1,
                mean=2.75,
                median=2.75,
                std=1.42,
                min=1.1,
                max=4.4,
                percentile25=2.2,
                percentile50=3.3,
                percentile75=3.3,
            ),
        ),
        (
            "int8_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "int16_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "int32_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "int64_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "int128_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "uint8_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "uint16_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "uint32_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
        (
            "uint64_col",
            NumericProfile(
                nulls_count=1,
                mean=2.5,
                median=2.5,
                std=1.29,
                min=1,
                max=4,
                percentile25=2,
                percentile50=3,
                percentile75=3,
            ),
        ),
    ],
)
def test_numeric_profile(
    numeric_test_data: polars.DataFrame,
    column_name: str,
    expected_profile: NumericProfile,
) -> None:
    profile = get_numeric_metrics(numeric_test_data, column_name)
    assert asdict(profile) == pytest.approx(asdict(expected_profile), rel=1e-3)
