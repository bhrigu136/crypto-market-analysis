"""Tests for CSV loading and schema validation."""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.loader import (
    FEAR_GREED_REQUIRED_COLUMNS,
    HISTORICAL_REQUIRED_COLUMNS,
    get_dataset_summary,
    load_fear_greed_data,
    load_historical_data,
    validate_required_columns,
)


class LoaderTests(unittest.TestCase):
    """Verify the public dataset-loading interface."""

    def setUp(self) -> None:
        """Create an isolated directory for temporary CSV fixtures."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_directory = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        """Remove temporary CSV fixtures."""
        self.temporary_directory.cleanup()

    def _write_csv(
        self,
        filename: str,
        columns: tuple[str, ...],
    ) -> Path:
        """Write a one-row CSV containing the requested columns."""
        file_path = self.fixture_directory / filename
        pd.DataFrame([{column: "sample" for column in columns}]).to_csv(
            file_path,
            index=False,
        )
        return file_path

    def test_load_historical_data_returns_dataframe(self) -> None:
        """Historical CSV loading should return a pandas DataFrame."""
        file_path = self._write_csv(
            "historical_data.csv",
            HISTORICAL_REQUIRED_COLUMNS,
        )

        result = load_historical_data(file_path)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), list(HISTORICAL_REQUIRED_COLUMNS))

    def test_load_fear_greed_data_returns_dataframe(self) -> None:
        """Fear & Greed CSV loading should return a pandas DataFrame."""
        file_path = self._write_csv(
            "fear_greed_index.csv",
            FEAR_GREED_REQUIRED_COLUMNS,
        )

        result = load_fear_greed_data(file_path)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), list(FEAR_GREED_REQUIRED_COLUMNS))

    def test_validate_required_columns_accepts_complete_schema(self) -> None:
        """Schema validation should accept all required columns."""
        dataframe = pd.DataFrame(columns=["account", "timestamp"])

        validate_required_columns(
            dataframe,
            ("account", "timestamp"),
            "Test data",
        )

    def test_validate_required_columns_reports_missing_columns(self) -> None:
        """Schema validation should identify every missing column."""
        dataframe = pd.DataFrame(columns=["account"])

        with self.assertRaisesRegex(
            ValueError,
            "Test data is missing required columns: timestamp, pnl",
        ):
            validate_required_columns(
                dataframe,
                ("account", "timestamp", "pnl"),
                "Test data",
            )

    def test_get_dataset_summary_returns_expected_types(self) -> None:
        """Dataset summaries should expose typed structural metrics."""
        dataframe = pd.DataFrame({"value": [1, 1], "label": ["a", "a"]})

        summary = get_dataset_summary(dataframe)

        self.assertIsInstance(summary, dict)
        self.assertEqual(summary["shape"], (2, 2))
        self.assertIsInstance(summary["duplicate_rows"], int)
        self.assertIsInstance(summary["memory_usage_bytes"], int)

    def test_missing_csv_raises_meaningful_error(self) -> None:
        """A missing CSV should raise an error containing the dataset name."""
        missing_path = self.fixture_directory / "missing.csv"

        with self.assertRaisesRegex(
            FileNotFoundError,
            "Historical trader data CSV file was not found",
        ):
            load_historical_data(missing_path)


if __name__ == "__main__":
    unittest.main()
