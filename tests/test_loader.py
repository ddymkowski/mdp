from pathlib import Path

import pytest
import polars as pl

from mdp.exceptions import UnsupportedDataFileExtension, UnsupportedDataTypeException
from mdp.cli.data_loader import DataReaderFactory, str_type_to_polars


def test_str_type_to_polars_valid() -> None:
    assert str_type_to_polars("Float32") == pl.Float32
    assert str_type_to_polars("Int64") == pl.Int64
    assert str_type_to_polars("String") == pl.String


def test_str_type_to_polars_invalid() -> None:
    with pytest.raises(
        UnsupportedDataTypeException, match="Unsupported datatype UnknownType"
    ):
        str_type_to_polars("UnknownType")


def test_data_reader_factory_csv() -> None:
    reader = DataReaderFactory.create(Path("data.csv"))
    assert reader == pl.read_csv


def test_data_reader_factory_parquet() -> None:
    reader = DataReaderFactory.create(Path("data.parquet"))
    assert reader == pl.read_parquet


def test_data_reader_factory_unsupported() -> None:
    with pytest.raises(
        UnsupportedDataFileExtension,
        match="Supported file extensions are: '.csv' and '.parquet'",
    ):
        DataReaderFactory.create(Path("data.txt"))
