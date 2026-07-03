# Crypto Market Analysis: Trader Performance and Market Sentiment

## Problem Statement

This project examines how trading activity and performance vary across Bitcoin
Fear & Greed Index conditions. The objective is to combine historical trade
records with daily market sentiment, explore the resulting dataset, and present
clear, reproducible observations. The project is exploratory; it does not make
predictions or claim that sentiment causes trading outcomes.

## Dataset Description

### Historical Trading Dataset

The historical dataset contains 211,224 Hyperliquid trade records across 16 raw
fields. It includes account and coin identifiers, execution price, token and USD
size, trade side and direction, timestamps, starting position, Closed PnL,
transaction and order identifiers, and fees. The data covers 32 accounts and
246 coins.

### Fear & Greed Dataset

The Fear & Greed dataset contains 2,644 daily observations with a numeric
sentiment value, a classification from Extreme Fear to Extreme Greed, a Unix
timestamp, and a calendar date.

The datasets are merged with a left join on `trade_date`, keeping the trading
dataset as the primary source. The final processed dataset contains 211,224 rows
and 21 columns. Six trade rows have no matching sentiment observation and remain
in the dataset with missing sentiment fields.

## Project Workflow

1. **Loading:** Load both CSV files through reusable functions and validate the
   expected schemas.
2. **Cleaning:** Standardize column names, remove exact duplicates, convert
   numeric and datetime fields, and derive `trade_date`.
3. **Merge:** Left join daily sentiment onto the historical trades and verify
   row preservation and sentiment coverage.
4. **EDA:** Examine sentiment, trading behaviour, trader performance, coin
   performance, and relationships between selected numeric variables.
5. **Insights:** Summarize descriptive patterns, limitations, and possible next
   steps without predictive or causal claims.

## Repository Structure

```text
crypto-market-analysis/
|-- data/
|   |-- raw/
|   |   |-- fear_greed_index.csv
|   |   `-- historical_data.csv
|   `-- processed/
|       `-- merged_dataset.csv
|-- notebooks/
|   `-- assignment_analysis.ipynb
|-- reports/
|   `-- final_report.md
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- loader.py
|   `-- preprocessing.py
|-- tests/
|   |-- test_loader.py
|   `-- test_preprocessing.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Pytest
- Jupyter Notebook

## Key Insights

- Greed is the most frequent sentiment on matched trade dates, appearing on 193
  of 479 dates (40.3%); Extreme Greed appears on 114 dates (23.8%).
- HYPE is the most traded coin with 68,005 records, representing 32.2% of all
  trade rows. @107 and BTC follow with 29,992 and 26,064 records.
- Sell records account for 51.38% of trades and buy records for 48.62%.
- Median Closed PnL is zero across every sentiment group. Average Closed PnL is
  highest during Extreme Greed (67.89) and lowest during Neutral conditions
  (34.31).
- Fear has the highest average trade size (7,816.11 USD) and average fee (1.50),
  while Extreme Greed has the lowest averages for both measures (3,112.25 USD
  and 0.68).
- @107 records the highest total Closed PnL (2.78 million), while TRUMP records
  the lowest (-364,824.91) in this dataset.
- Size USD and fee have the strongest displayed numeric correlation (0.746).
  Closed PnL has weak correlations with Size USD (0.124), fee (0.084), and the
  Fear & Greed value (0.008).

These findings describe the supplied records and should not be interpreted as
evidence of causation.

## Installation

Python 3.10 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

Start Jupyter from the project root:

```powershell
jupyter notebook notebooks/assignment_analysis.ipynb
```

Open the notebook and select **Run All** to reproduce data loading, cleaning,
merge validation, and the EDA. To run the automated checks:

```powershell
python -m pytest
```

## Future Improvements

- Evaluate carefully validated machine-learning models for profitability or
  risk classification after defining a leakage-safe prediction target.
- Build an interactive dashboard for filtering by account, coin, date, and
  sentiment.
- Incorporate real-time trade and sentiment data for continuously updated
  monitoring.
- Add market indicators such as price returns, volatility, volume, funding
  rates, and open interest.
- Compare results across longer time periods and a broader trader population.

## License

This project is available under the MIT License
