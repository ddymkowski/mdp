# Data Quality Profiler

## Overview
The `pldmp` package provides an efficient and scalable way to perform data profiling using the Polars library. It analyzes datasets to generate various statistical summaries and insights, helping users understand the structure and quality of their data.

## Features
- Supports a variety of data types, including numeric, string, and datetime.
- Computes key statistical metrics such as mean, median, standard deviation, and percentiles.
- Detects missing values, empty fields, and string token distributions.
- Provides both a Python and a command-line interface (CLI) for easy usage.

## Installation
```bash
pip install plmdp
```

## Usage

### Python Example
```python
from pathlib import Path
from pprint import pprint
import polars as pl
from dq import Profiler

if __name__ == "__main__":
    datafile_path = Path(__file__).resolve().parent / "data.csv"
    data: pl.DataFrame = pl.read_csv(datafile_path, separator=";")
    results = Profiler().run_profiling(data)
    pprint(results)
```

### CLI Example
```bash
#!/bin/bash

DATA_PATH="$(pwd)/data.csv"
SCHEMA='{"comment": "String", "dob": "Date", "sales": "Float32"}'
LOADER_KWARGS='{"separator":";"}'
FORMATTER='json'

dq --path "$DATA_PATH" --schema="$SCHEMA" --kwargs="$LOADER_KWARGS" --format="$FORMATTER"
```

## Supported Data Types
The package supports the following Polars data types:
- Numeric: `Float32`, `Float64`, `Int8`, `Int16`, `Int32`, `Int64`, `Int128`, `UInt8`, `UInt16`, `UInt32`, `UInt64`, `Decimal`
- String: `String`, `Categorical`
- Date/Time: `Date`, `Datetime`
- Others: `Boolean`

## Metrics Computed
- **String Profile**: Minimum/maximum/average string length, token counts, empty or whitespace count.
- **Numeric Profile**: Mean, median, standard deviation, min/max values, and percentiles.
- **Date/Datetime Profile**: Minimum and maximum values.
- **Base Profile**: Null values count.

## License
MIT License

