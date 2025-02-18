from typing import cast

import polars

from mdp.constants import FLOATING_POINT
from mdp.models.numeric import NumericProfile
from mdp.primitives import OptionalNumeric


def get_numeric_metrics(
    dataframe: polars.DataFrame,
    column_name: str,
) -> NumericProfile:
    column = dataframe[column_name]
    null_count = column.null_count()
    mean = cast(OptionalNumeric, column.mean())
    median = cast(OptionalNumeric, column.median())
    std = cast(OptionalNumeric, column.std())
    min_value = cast(OptionalNumeric, column.min())
    max_value = cast(OptionalNumeric, column.max())

    percentile25 = cast(OptionalNumeric, column.quantile(0.25))
    percentile50 = cast(OptionalNumeric, column.quantile(0.50))
    percentile75 = cast(OptionalNumeric, column.quantile(0.75))

    return NumericProfile(
        nulls_count=null_count,
        mean=round(mean, FLOATING_POINT) if mean is not None else None,
        median=round(median, FLOATING_POINT) if median is not None else None,
        std=round(std, FLOATING_POINT) if std is not None else None,
        min=round(min_value, FLOATING_POINT) if min_value is not None else None,
        max=round(max_value, FLOATING_POINT) if max_value is not None else None,
        percentile25=round(percentile25, FLOATING_POINT)
        if percentile25 is not None
        else None,
        percentile50=round(percentile50, FLOATING_POINT)
        if percentile50 is not None
        else None,
        percentile75=round(percentile75, FLOATING_POINT)
        if percentile75 is not None
        else None,
    )
