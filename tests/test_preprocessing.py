"""Tests for dataset cleaning, merging, and validation."""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.preprocessing import (
    clean_fear_greed_data,
    clean_historical_data,
    merge_datasets,
    save_processed_dataset,
    standardize_column_names,
    validate_merge,
)


def _historical_record() -> dict[str, object]:
    """Return a representative raw historical trade record."""
    return {
        "Account": "0xabc",
        "Coin": "BTC",
        "Execution Price": "95000.5",
        "Size Tokens": "0.01",
        "Size USD": "950.005",
        "Side": "BUY",
        "Timestamp IST": "02-12-2024 22:50",
        "Start Position": "0",
        "Direction": "Buy",
        "Closed PnL": "12.5",
        "Transaction Hash": "0xtransaction",
        "Order ID": "12345",
        "Crossed": True,
        "Fee": "0.25",
        "Trade ID": "67890",
        "Timestamp": "1733179800000",
    }


def _fear_greed_record(
    date: str = "2024-12-02",
    classification: str = "Greed",
) -> dict[str, object]:
    """Return a representative raw sentiment record."""
    return {
        "timestamp": "1733097600",
        "value": "75",
        "classification": classification,
        "date": date,
    }


class PreprocessingTests(unittest.TestCase):
    """Verify deterministic cleaning and left-join behavior."""

    def test_standardize_column_names_uses_snake_case(self) -> None:
        """Column labels should be normalized without changing values."""
        dataframe = pd.DataFrame(
            {"Closed PnL": [1.5], "Timestamp IST": ["value"]}
        )

        result = standardize_column_names(dataframe)

        self.assertEqual(list(result.columns), ["closed_pnl", "timestamp_ist"])
        self.assertEqual(result.loc[0, "closed_pnl"], 1.5)

    def test_clean_historical_data_removes_exact_duplicates(self) -> None:
        """Exact duplicate rows should be removed once."""
        record = _historical_record()
        dataframe = pd.DataFrame([record, record.copy()])

        result = clean_historical_data(dataframe)

        self.assertEqual(len(result), 1)
        self.assertEqual(int(result.duplicated().sum()), 0)

    def test_clean_historical_data_converts_types_and_date(self) -> None:
        """Timestamps and numeric values should receive usable data types."""
        result = clean_historical_data(pd.DataFrame([_historical_record()]))

        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(result["timestamp"])
        )
        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(result["timestamp_ist"])
        )
        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(result["trade_date"])
        )
        self.assertTrue(pd.api.types.is_numeric_dtype(result["closed_pnl"]))
        self.assertEqual(result.loc[0, "trade_date"], pd.Timestamp("2024-12-02"))

    def test_clean_fear_greed_data_converts_types_and_date(self) -> None:
        """Sentiment dates and values should be converted without row loss."""
        result = clean_fear_greed_data(
            pd.DataFrame([_fear_greed_record()])
        )

        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result["date"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(result["value"]))
        self.assertEqual(result.loc[0, "trade_date"], pd.Timestamp("2024-12-02"))

    def test_merge_preserves_historical_rows(self) -> None:
        """The historical dataset must remain the left-side source of truth."""
        first_trade = _historical_record()
        second_trade = {**first_trade, "Order ID": "12346"}
        historical = clean_historical_data(
            pd.DataFrame([first_trade, second_trade])
        )
        sentiment = clean_fear_greed_data(
            pd.DataFrame([_fear_greed_record()])
        )

        merged = merge_datasets(historical, sentiment)
        validation = validate_merge(historical, merged)

        self.assertEqual(len(merged), len(historical))
        self.assertEqual(validation["row_difference"], 0)
        self.assertEqual(validation["missing_sentiment_rows"], 0)
        self.assertEqual(validation["merge_success_rate_percent"], 100.0)

    def test_merge_keeps_unmatched_historical_rows(self) -> None:
        """A missing sentiment date should produce nulls, not row loss."""
        historical = clean_historical_data(
            pd.DataFrame([_historical_record()])
        )
        sentiment = clean_fear_greed_data(
            pd.DataFrame([_fear_greed_record(date="2024-12-03")])
        )

        merged = merge_datasets(historical, sentiment)
        validation = validate_merge(historical, merged)

        self.assertEqual(len(merged), 1)
        self.assertEqual(validation["missing_sentiment_rows"], 1)
        self.assertEqual(validation["merge_success_rate_percent"], 0.0)

    def test_save_processed_dataset_writes_csv(self) -> None:
        """Processed output should be written without a dataframe index."""
        dataframe = pd.DataFrame({"trade_date": ["2024-12-02"]})
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "merged.csv"

            saved_path = save_processed_dataset(dataframe, output_path)
            reloaded = pd.read_csv(saved_path)

        self.assertEqual(list(reloaded.columns), ["trade_date"])
        self.assertEqual(len(reloaded), 1)


if __name__ == "__main__":
    unittest.main()
