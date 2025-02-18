from pathlib import Path
from pprint import pprint

from plmdp import Profiler
import polars


if __name__ == "__main__":
    datafile_path = Path(__file__).resolve().parent / "data.csv"
    data: polars.DataFrame = polars.read_csv(datafile_path, separator=";")
    results = Profiler().run_profiling(data)
    pprint(results)
