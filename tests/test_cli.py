import argparse
from pathlib import Path

import pytest
import json
from unittest.mock import patch, MagicMock

from polars import Int64, String

from plmdp.cli.cli import load_schema_from_cli, load_kwargs, main
from plmdp.exceptions import UnsupportedDataTypeException
from plmdp.models.output import ProfilerOutput
from tests.test_profiler import profiler_output  # noqa: F401


def test_load_schema_from_cli_valid() -> None:
    schema_json = json.dumps({"column1": "Int64", "column2": "String"})
    result = load_schema_from_cli(schema_json)
    assert result == {"column1": Int64, "column2": String}


def test_load_schema_from_cli_invalid_json() -> None:
    with pytest.raises(ValueError, match="Schema is not valid json"):
        load_schema_from_cli("{]")


def test_load_schema_from_cli_unsupported_data_type() -> None:
    with pytest.raises(UnsupportedDataTypeException):
        load_schema_from_cli(json.dumps({"column1": "InvalidType"}))


def test_load_schema_from_cli_none() -> None:
    assert load_schema_from_cli(None) is None


def test_load_kwargs_valid() -> None:
    kwargs_json = json.dumps({"sep": ",", "header": True})
    result = load_kwargs(kwargs_json)
    assert result == {"sep": ",", "header": True}


def test_load_kwargs_invalid_json() -> None:
    with pytest.raises(ValueError, match="Kwargs are invalid json"):
        load_kwargs("invalid_json")


@patch("argparse.ArgumentParser.parse_args")
@patch("plmdp.cli.data_loader.DataReaderFactory.create")
@patch("plmdp.profiler.Profiler.run_profiling")
@patch("plmdp.cli.formatter.FormatterFactory.get_formatter")
def test_main_with_formatters(
        mock_get_formatter: MagicMock,
        mock_run_profiling: MagicMock,
        mock_data_reader: MagicMock,
        mock_parse_args: MagicMock,
        profiler_output: ProfilerOutput,  # noqa: F811
) -> None:
    mock_parse_args.return_value = argparse.Namespace(
        path="/fake/path.csv", schema=None, kwargs=None, columns_to_ignore=None, formatter="json"
    )

    mock_data_reader.return_value = lambda source, schema, **kwargs: "mock_dataframe"
    mock_run_profiling.return_value = profiler_output

    mock_formatter = MagicMock()
    mock_get_formatter.return_value = mock_formatter

    mock_parse_args.return_value.formatter = "json"
    main()
    mock_get_formatter.assert_called_with("json")
    mock_formatter.assert_called_with(profiler_output)

    mock_data_reader.assert_called_with(Path("/fake/path.csv"))
    mock_run_profiling.assert_called_with("mock_dataframe", columns_to_ignore=[])
