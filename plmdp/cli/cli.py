import argparse
import json
from pathlib import Path
from typing import Any, cast

import polars.datatypes

from plmdp.cli.formatter import FormatterFactory
from plmdp.exceptions import UnsupportedDataTypeException
from plmdp.cli.data_loader import str_type_to_polars, DataReaderFactory
from plmdp.models.output import ProfilerOutput
from plmdp.primitives import ColumnName
from plmdp.profiler import Profiler


def load_schema_from_cli(
    schema: str | None,
) -> dict[ColumnName, polars.datatypes.DataTypeClass] | None:
    if not schema:
        return None
    try:
        json_input = json.loads(schema)
        return {k: str_type_to_polars(v) for k, v in json_input.items()}

    except json.JSONDecodeError as e:
        raise ValueError("Schema is not valid json") from e

    except UnsupportedDataTypeException:
        raise


def load_kwargs(kwargs_str: str | None) -> dict[Any, Any]:
    if not kwargs_str:
        return {}
    try:
        return cast(dict[Any, Any], json.loads(kwargs_str))
    except json.JSONDecodeError as e:
        raise ValueError("Kwargs are invalid json") from e


def main() -> str:
    parser = argparse.ArgumentParser(description="Profiler cli")

    parser.add_argument("-p", "--path", required=True, help="Path to datafile")

    parser.add_argument(
        "-s", "--schema", required=False, help="Dataframe schema as json"
    )

    parser.add_argument(
        "-k", "--kwargs", required=False, help="Polars dataframe loader kwargs"
    )

    parser.add_argument(
        "-c", "--columns-to-ignore", required=False, help="Column names to ignore"
    )

    parser.add_argument(
        "-f",
        "--formatter",
        required=False,
        default="json",
        help="Stdout format: json, yaml or raw",
    )
    args = parser.parse_args()
    str_schema = args.schema
    path = Path(args.path)
    dataloader_kwargs = args.kwargs
    columns_to_ignore = (
        args.columns_to_ignore.split(",") if args.columns_to_ignore else []
    )

    schema = load_schema_from_cli(str_schema)
    kwargs = load_kwargs(dataloader_kwargs)
    stdout_format = args.formatter

    read_data = DataReaderFactory.create(path)
    data = read_data(source=path, schema=schema, **kwargs)
    results: ProfilerOutput = Profiler().run_profiling(
        data, columns_to_ignore=columns_to_ignore
    )
    formatter = FormatterFactory.get_formatter(stdout_format)
    return formatter(results)


if __name__ == "__main__":
    print(main())
