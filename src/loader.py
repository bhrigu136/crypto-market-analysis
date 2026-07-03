"""Dataset loading and schema-inspection utilities."""

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import FEAR_GREED_DATA_PATH, HISTORICAL_DATA_PATH


HISTORICAL_REQUIRED_COLUMNS: tuple[str, ...] = (
    "Account",
    "Coin",
    "Execution Price",
    "Size Tokens",
    "Size USD",
    "Side",
    "Timestamp IST",
    "Start Position",
    "Direction",
    "Closed PnL",
    "Transaction Hash",
    "Order ID",
    "Crossed",
    "Fee",
    "Trade ID",
    "Timestamp",
)

FEAR_GREED_REQUIRED_COLUMNS: tuple[str, ...] = (
    "timestamp",
    "value",
    "classification",
    "date",
)


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: Iterable[str],
    dataset_name: str = "dataset",
) -> None:
    """Ensure that a dataframe contains every required column.

    Args:
        dataframe: Dataframe whose schema should be checked.
        required_columns: Column names that must be present.
        dataset_name: Human-readable name included in error messages.

    Raises:
        TypeError: If ``dataframe`` is not a pandas DataFrame.
        ValueError: If one or more required columns are missing.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame")

    missing_columns = [
        column for column in required_columns if column not in dataframe.columns
    ]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"{dataset_name} is missing required columns: {missing_text}"
        )


def _load_csv(file_path: Path, dataset_name: str) -> pd.DataFrame:
    """Load a CSV file without changing its values or inferred data types."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"{dataset_name} CSV file was not found at: {path.resolve()}"
        )

    try:
        return pd.read_csv(path, low_memory=False)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"{dataset_name} CSV file is empty: {path}") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(
            f"{dataset_name} CSV file could not be parsed: {path}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"{dataset_name} CSV file is not valid UTF-8: {path}"
        ) from exc


def load_historical_data(
    file_path: Path | None = None,
) -> pd.DataFrame:
    """Load historical trader data and validate its expected schema.

    Args:
        file_path: Optional CSV location. The configured raw-data path is used
            when no path is supplied.

    Returns:
        The unmodified historical trader dataset.
    """
    path = file_path if file_path is not None else HISTORICAL_DATA_PATH
    dataframe = _load_csv(path, "Historical trader data")
    validate_required_columns(
        dataframe,
        HISTORICAL_REQUIRED_COLUMNS,
        "Historical trader data",
    )
    return dataframe


def load_fear_greed_data(
    file_path: Path | None = None,
) -> pd.DataFrame:
    """Load Fear & Greed Index data and validate its expected schema.

    Args:
        file_path: Optional CSV location. The configured raw-data path is used
            when no path is supplied.

    Returns:
        The unmodified Fear & Greed Index dataset.
    """
    path = file_path if file_path is not None else FEAR_GREED_DATA_PATH
    dataframe = _load_csv(path, "Fear & Greed Index data")
    validate_required_columns(
        dataframe,
        FEAR_GREED_REQUIRED_COLUMNS,
        "Fear & Greed Index data",
    )
    return dataframe


def get_dataset_summary(dataframe: pd.DataFrame) -> dict[str, Any]:
    """Return structural and data-quality metrics for a dataframe.

    The function only inspects the supplied data. It does not mutate values,
    convert data types, remove rows, or fill missing data.

    Args:
        dataframe: Dataset to inspect.

    Returns:
        A dictionary containing shape, schema, memory, missing-value,
        duplicate-row, and cardinality information.

    Raises:
        TypeError: If ``dataframe`` is not a pandas DataFrame.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame")

    memory_by_column = dataframe.memory_usage(index=False, deep=True)
    return {
        "shape": dataframe.shape,
        "columns": dataframe.columns.tolist(),
        "dtypes": dataframe.dtypes.astype(str).to_dict(),
        "memory_usage_bytes": int(
            dataframe.memory_usage(index=True, deep=True).sum()
        ),
        "memory_usage_by_column_bytes": {
            column: int(value)
            for column, value in memory_by_column.items()
        },
        "missing_values": {
            column: int(value)
            for column, value in dataframe.isna().sum().items()
        },
        "duplicate_rows": int(dataframe.duplicated().sum()),
        "unique_values": {
            column: int(value)
            for column, value in dataframe.nunique(dropna=False).items()
        },
    }
