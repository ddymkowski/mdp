import json
import datetime
import pytest
import yaml

from plmdp.cli.formatter import FormatterFactory
from plmdp.models import DateOrDateTimeProfile, NumericProfile
from plmdp.models.output import ProfilerOutput, ColumnData


@pytest.fixture
def profiler_output_unfrozen() -> ProfilerOutput:
    return ProfilerOutput(
        rows_count=20,
        column_count=3,
        ignored_columns=["comment"],
        dataframe_size=545,
        columns=[
            ColumnData(
                name="dob",
                type="Date",
                metrics=DateOrDateTimeProfile(
                    nulls_count=0,
                    min=datetime.date(1973, 9, 19),
                    max=datetime.date(1999, 8, 29),
                ),
            ),
            ColumnData(
                name="sales",
                type="Float32",
                metrics=NumericProfile(
                    nulls_count=0,
                    mean=181.5,
                    median=185.0,
                    std=78.42,
                    min=50.0,
                    max=320.0,
                    percentile25=120.0,
                    percentile50=190.0,
                    percentile75=230.0,
                ),
            ),
        ],
    )


def test_get_formatter_json(profiler_output_unfrozen: ProfilerOutput) -> None:
    formatter = FormatterFactory.get_formatter("json")
    formatted_output = formatter(profiler_output_unfrozen)

    assert isinstance(formatted_output, str)
    assert json.loads(formatted_output)


def test_get_formatter_yaml(profiler_output_unfrozen: ProfilerOutput) -> None:
    formatter = FormatterFactory.get_formatter("yaml")
    formatted_output = formatter(profiler_output_unfrozen)

    assert isinstance(formatted_output, str)
    assert yaml.safe_load(formatted_output)


def test_get_formatter_invalid() -> None:
    with pytest.raises(ValueError, match="Unsupported format. Use 'json' or 'yaml'."):
        FormatterFactory.get_formatter("xml")  # type: ignore
