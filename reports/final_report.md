# Final Report: Crypto Market Analysis

## Executive Summary

Historical Hyperliquid trades were combined with the Bitcoin Fear & Greed
Index to examine activity and performance across sentiment conditions. The
final dataset preserves all 211,224 trades and matches sentiment to 211,218 of
them (99.9972%). Results are descriptive and do not establish causation.

## Methodology

- Validated schemas, types, missing values and duplicates.
- Standardized columns and converted numeric and datetime fields.
- Created `trade_date` from the IST timestamp.
- Left joined daily sentiment onto trades.
- Analyzed sentiment, activity, PnL, fees, trade size, coins and correlations.

## Cleaning

No exact duplicate rows or source missing values were found. All raw rows were
retained. Repeated order IDs and transaction hashes were reported but not
removed because they can represent separate fills. The numeric source timestamp
had limited precision, so `Timestamp IST` was used to derive `trade_date`.

## Merge

| Measure | Result |
|---|---:|
| Rows before and after merge | 211,224 |
| Matched sentiment rows | 211,218 |
| Missing sentiment rows | 6 |
| Match rate | 99.9972% |

The six unmatched trades from 26 October 2024 remain in the dataset.

## EDA

The EDA uses only the merged dataset. It covers sentiment frequency, trading
behaviour, PnL, fees, trade size, coin performance and selected correlations.
Outlier-heavy charts use stated display limits or fixed samples for readability;
reported correlations use the full dataset.

## Key Findings

- Greed appears on 193 of 479 matched trade dates (40.3%).
- HYPE is the most traded coin with 68,005 records (32.2%).
- Sell trades represent 51.38% of rows and buy trades 48.62%.
- Average Closed PnL ranges from 34.31 in Neutral to 67.89 in Extreme Greed;
  every sentiment group has a median of zero.
- Fear has the highest average trade size (7,816.11 USD) and fee (1.50).
- Size USD and fee have a 0.746 correlation. Closed PnL has weak correlations
  with size (0.124), fee (0.084) and sentiment value (0.008).

## Limitations

- Daily sentiment cannot capture intraday changes.
- The sample contains 32 accounts and may not represent the wider market.
- Closed PnL is highly skewed and sensitive to outliers.
- External market indicators are absent; correlations are not causal evidence.

## Recommendations

- Add intraday sentiment and market data.
- Report robust statistics alongside means.
- Segment future work by coin, account and position type.
- Use time-based validation and leakage controls if predictive modeling is added.
