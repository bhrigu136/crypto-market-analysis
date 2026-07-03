# Final Report: Crypto Market Analysis

## Executive Summary

This project evaluates the relationship between historical Hyperliquid trading
records and the Bitcoin Fear & Greed Index. Two source datasets were validated,
cleaned, and joined by calendar date. The final dataset preserves all 211,224
trade rows and contains 21 columns. Sentiment was matched to 211,218 rows,
producing a 99.9972% match rate; six trades on 26 October 2024 have no matching
sentiment observation.

The exploratory analysis describes differences in trade activity, Closed PnL,
fees, and trade size across sentiment groups and coins. Results are descriptive
and do not establish causation or provide a predictive trading strategy.

## Methodology

1. Loaded the historical trading and Fear & Greed CSV files using reusable
   loader functions.
2. Validated required columns, shapes, inferred data types, missing values,
   duplicate rows, cardinality, and memory usage.
3. Standardized column names and converted numeric and datetime fields.
4. Derived a daily `trade_date` from the historical IST timestamp and the
   sentiment date.
5. Left joined sentiment onto the historical trades and validated row counts
   and coverage.
6. Performed exploratory analysis using Matplotlib and Seaborn, covering market
   sentiment, trading behaviour, trader performance, coin performance, and
   selected numeric relationships.

## Cleaning

Neither raw dataset contained missing values or exact duplicate rows, so all
211,224 historical records and 2,644 sentiment records remained after exact
deduplication. Historical columns were converted to snake_case; numeric trade
fields were coerced to numeric types; `Timestamp IST` and `Timestamp` were
parsed as datetimes; and `trade_date` was derived from `Timestamp IST`.

The Fear & Greed date was parsed as a datetime, its value and timestamp were
kept numeric, classification was kept as text, and a normalized `trade_date`
was created. Repeated order IDs and transaction hashes were reported but not
removed because they are not, by themselves, exact duplicate trade rows.

## Merge

The cleaned historical data was left joined with the cleaned sentiment data on
`trade_date`. The merge preserved all 211,224 historical rows. Sentiment fields
were populated for 211,218 rows, while six rows dated 26 October 2024 remained
unmatched. These rows were retained with missing sentiment values rather than
being discarded.

| Validation measure | Result |
|---|---:|
| Historical rows before merge | 211,224 |
| Rows after merge | 211,224 |
| Row difference | 0 |
| Matched sentiment rows | 211,218 |
| Missing sentiment rows | 6 |
| Merge success rate | 99.9972% |

## EDA

The EDA uses only the processed merged dataset. Daily sentiment distributions
are calculated from one sentiment record per trade date to prevent busy trading
days from inflating the sentiment-day counts. Trade-level charts examine coin
frequency, buy and sell sides, long and short direction labels, daily activity,
Closed PnL, fees, and USD trade size.

Because Closed PnL and trade-size distributions contain large outliers, the PnL
histogram displays the 1st through 99th percentiles, boxplots hide only outlier
markers, and dense relationship plots use a fixed 15,000-row sample with
logarithmic display scales. Reported correlations are calculated from the full
dataset rather than from the plotted sample.

## Key Findings

1. Greed is recorded on 193 of 479 matched trade dates (40.3%), and Extreme
   Greed on 114 dates (23.8%). Extreme Fear occurs on 14 dates (2.9%).
2. HYPE is the most frequently traded coin with 68,005 records (32.2%), followed
   by @107 with 29,992 and BTC with 26,064.
3. Sell trades represent 51.38% of rows, compared with 48.62% for buy trades.
   Among direction labels containing Long or Short, 56.54% contain Long and
   43.46% contain Short.
4. Median Closed PnL is zero in every sentiment group. Average Closed PnL ranges
   from 34.31 during Neutral conditions to 67.89 during Extreme Greed.
5. Fear has the largest average USD trade size (7,816.11) and average fee (1.50).
   Extreme Greed has the smallest averages for both (3,112.25 and 0.68).
6. @107 has the highest total Closed PnL at 2.78 million. TRUMP has the lowest
   total at -364,824.91.
7. The strongest displayed correlation is between Size USD and fee (0.746).
   Closed PnL has weak linear correlations with Size USD (0.124), fee (0.084),
   and Fear & Greed value (0.008).

## Limitations

- Sentiment is measured daily, while trades occur intraday. A single daily value
  cannot describe sentiment changes within the day.
- The analysis contains only the supplied trader population: 32 accounts and
  246 coins. It may not represent the wider market.
- Six trade rows do not have a matching sentiment observation.
- The numeric source timestamp has limited precision, so `Timestamp IST` is used
  to derive the merge date.
- Closed PnL is highly skewed and includes large outliers; group means can be
  sensitive to those observations.
- Market returns, volatility, volume, funding rates, and other external factors
  are not included.
- The work is exploratory. Correlation does not establish causation, and no
  predictive model or out-of-sample validation is included.

## Recommendations

- Validate and document the missing sentiment date before using the dataset in
  downstream modeling.
- Report medians, quantiles, sample sizes, and robust statistics alongside means
  when comparing PnL across groups.
- Segment future analysis by coin, account, and position type to distinguish
  broad patterns from activity concentrated in a few categories.
- Add intraday market data and additional indicators before investigating
  short-horizon relationships.
- If prediction is pursued, define a forward-looking target, prevent temporal
  leakage, and evaluate models on later time periods rather than random splits.
