"""Cleaning, merge, and validation utilities for the source datasets."""

from collections.abc import Iterable
from pathlib import Path
import re
from typing import Any

import pandas as pd

from src.config import MERGED_DATASET_PATH
from src.loader import (
    FEAR_GREED_REQUIRED_COLUMNS,
    HISTORICAL_REQUIRED_COLUMNS,
    validate_required_columns,
)


HISTORICAL_NUMERIC_COLUMNS: tuple[str, ...] = (
    "execution_price",
    "size_tokens",
    "size_usd",
    "start_position",
    "closed_pnl",
    "order_id",
    "fee",
    "trade_id",
)

FEAR_GREED_PREFIX = "fear_greed_"


def _to_snake_case(column_name: object) -> str:
    """Convert a column label to a normalized snake_case name."""
    text = str(column_name).strip().replace("&", " and ")
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z][a-z])", "_", text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    return text.strip("_").lower()


def standardize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with column names converted to snake_case.

    Raises:
        TypeError: If ``dataframe`` is not a pandas DataFrame.
        ValueError: If standardization creates blank or duplicate names.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame")

    standardized = dataframe.copy()
    column_names = [_to_snake_case(column) for column in standardized.columns]
    if any(not column for column in column_names):
        raise ValueError("Column names cannot be blank after standardization")
    if len(column_names) != len(set(column_names)):
        raise ValueError(
            "Column-name standardization produced duplicate column names"
        )

    standardized.columns = column_names
    return standardized


def create_trade_date(
    dataframe: pd.DataFrame,
    timestamp_column: str,
) -> pd.DataFrame:
    """Create a normalized ``trade_date`` from a datetime column.

    The source timestamp is retained unchanged.

    Raises:
        KeyError: If the requested timestamp column does not exist.
        TypeError: If the source column is not datetime-like.
    """
    if timestamp_column not in dataframe.columns:
        raise KeyError(f"Timestamp column not found: {timestamp_column}")
    if not pd.api.types.is_datetime64_any_dtype(
        dataframe[timestamp_column].dtype
    ):
        raise TypeError(
            f"{timestamp_column} must be converted to datetime first"
        )

    dated = dataframe.copy()
    dated["trade_date"] = dated[timestamp_column].dt.normalize()
    return dated


def clean_historical_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean historical trades without aggregating or discarding valid rows.

    Exact duplicate rows are removed. Columns are standardized, numeric fields
    are converted, both timestamps are parsed, and ``trade_date`` is derived
    from the local ``Timestamp IST`` value.
    """
    validate_required_columns(
        dataframe,
        HISTORICAL_REQUIRED_COLUMNS,
        "Historical trader data",
    )
    cleaned = standardize_column_names(dataframe.drop_duplicates())

    for column in HISTORICAL_NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    numeric_timestamp = pd.to_numeric(cleaned["timestamp"], errors="coerce")
    cleaned["timestamp"] = pd.to_datetime(
        numeric_timestamp,
        unit="ms",
        errors="coerce",
        utc=True,
    )
    cleaned["timestamp_ist"] = pd.to_datetime(
        cleaned["timestamp_ist"],
        format="%d-%m-%Y %H:%M",
        errors="coerce",
    )
    return create_trade_date(cleaned, "timestamp_ist")


def clean_fear_greed_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean Fear & Greed data and derive its merge date."""
    validate_required_columns(
        dataframe,
        FEAR_GREED_REQUIRED_COLUMNS,
        "Fear & Greed Index data",
    )
    cleaned = standardize_column_names(dataframe.drop_duplicates())
    cleaned["timestamp"] = pd.to_numeric(
        cleaned["timestamp"],
        errors="coerce",
    )
    cleaned["value"] = pd.to_numeric(cleaned["value"], errors="coerce")
    cleaned["classification"] = cleaned["classification"].astype("string")
    cleaned["date"] = pd.to_datetime(
        cleaned["date"],
        format="%Y-%m-%d",
        errors="coerce",
    )
    return create_trade_date(cleaned, "date")


def get_cleaning_summary(
    original: pd.DataFrame,
    cleaned: pd.DataFrame,
    identifier_columns: Iterable[str] = (),
) -> dict[str, Any]:
    """Summarize row, missing-value, type, and identifier changes."""
    if not isinstance(original, pd.DataFrame) or not isinstance(
        cleaned,
        pd.DataFrame,
    ):
        raise TypeError("original and cleaned must be pandas DataFrames")

    identifier_summary: dict[str, dict[str, int]] = {}
    for column in identifier_columns:
        if column not in cleaned.columns:
            raise KeyError(f"Identifier column not found: {column}")
        duplicate_mask = cleaned[column].notna() & cleaned.duplicated(
            subset=[column],
            keep=False,
        )
        identifier_summary[column] = {
            "duplicate_rows": int(duplicate_mask.sum()),
            "duplicate_values": int(
                cleaned.loc[duplicate_mask, column].nunique()
            ),
        }

    return {
        "rows_before": len(original),
        "rows_after": len(cleaned),
        "rows_removed": len(original) - len(cleaned),
        "missing_values_before": int(original.isna().sum().sum()),
        "missing_values_after": int(cleaned.isna().sum().sum()),
        "columns_after": cleaned.columns.tolist(),
        "dtypes_after": cleaned.dtypes.astype(str).to_dict(),
        "identifier_duplicates": identifier_summary,
    }


def merge_datasets(
    historical_data: pd.DataFrame,
    fear_greed_data: pd.DataFrame,
) -> pd.DataFrame:
    """Left join cleaned trades to one sentiment record per trade date.

    Fear & Greed columns are prefixed in the output to keep their origin clear
    and prevent collisions with historical columns.
    """
    validate_required_columns(
        historical_data,
        ("trade_date",),
        "Clean historical trader data",
    )
    validate_required_columns(
        fear_greed_data,
        ("trade_date", "classification", "value"),
        "Clean Fear & Greed Index data",
    )
    if fear_greed_data["trade_date"].duplicated().any():
        raise ValueError(
            "Fear & Greed data must contain one row per trade_date"
        )

    sentiment_columns = {
        column: f"{FEAR_GREED_PREFIX}{column}"
        for column in fear_greed_data.columns
        if column != "trade_date"
    }
    sentiment_data = fear_greed_data.rename(columns=sentiment_columns)
    return historical_data.merge(
        sentiment_data,
        how="left",
        on="trade_date",
        sort=False,
        validate="many_to_one",
    )


def validate_merge(
    historical_data: pd.DataFrame,
    merged_data: pd.DataFrame,
) -> dict[str, int | float]:
    """Validate row preservation and sentiment coverage after the left join.

    Raises:
        ValueError: If the merge changed the historical row count.
    """
    sentiment_column = f"{FEAR_GREED_PREFIX}classification"
    validate_required_columns(
        merged_data,
        ("trade_date", sentiment_column),
        "Merged data",
    )

    rows_before = len(historical_data)
    rows_after = len(merged_data)
    if rows_after != rows_before:
        raise ValueError(
            "Merge integrity failure: historical row count changed from "
            f"{rows_before} to {rows_after}"
        )

    missing_sentiment_rows = int(merged_data[sentiment_column].isna().sum())
    matched_sentiment_rows = rows_after - missing_sentiment_rows
    success_rate = (
        matched_sentiment_rows / rows_after * 100 if rows_after else 0.0
    )
    return {
        "rows_before_merge": rows_before,
        "rows_after_merge": rows_after,
        "row_difference": rows_after - rows_before,
        "matched_sentiment_rows": matched_sentiment_rows,
        "missing_sentiment_rows": missing_sentiment_rows,
        "merge_success_rate_percent": round(success_rate, 4),
    }


def save_processed_dataset(
    dataframe: pd.DataFrame,
    output_path: Path | None = None,
) -> Path:
    """Save a processed dataframe as CSV and return the resolved path."""
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame")

    path = Path(output_path) if output_path is not None else MERGED_DATASET_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)
    return path.resolve()
