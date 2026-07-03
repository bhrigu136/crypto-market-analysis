# Crypto Market Analysis

## Problem Statement

This project explores how trader activity and performance vary with the Bitcoin
Fear & Greed Index. It is descriptive analysis, not a trading strategy or
prediction system.

## Dataset Description

| Dataset | Contents | Size |
|---|---|---:|
| Historical trades | Coin, side, direction, size, fee, timestamps and Closed PnL | 211,224 rows |
| Fear & Greed Index | Daily sentiment value, classification and date | 2,644 rows |
| Processed dataset | Left-joined trade and sentiment data | 211,224 rows, 21 columns |

The merge matched sentiment to 211,218 trades. Six unmatched trades were kept
with missing sentiment values.

## Project Workflow

1. Load and validate both datasets.
2. Standardize columns and convert numeric and datetime fields.
3. Create `trade_date` and left join sentiment onto trades.
4. Validate row preservation and sentiment coverage.
5. Explore sentiment, behaviour, performance, coins and numeric relationships.

## Repository Structure

```text
crypto-market-analysis/
|-- data/
|   |-- raw/
|   `-- processed/merged_dataset.csv
|-- notebooks/assignment_analysis.ipynb
|-- reports/final_report.md
|-- src/
|   |-- config.py
|   |-- loader.py
|   `-- preprocessing.py
|-- tests/
|-- README.md
|-- requirements.txt
`-- LICENSE
```

## Technologies Used

Python, Pandas, NumPy, Matplotlib, Seaborn, Pytest and Jupyter Notebook.

## Key Insights

- Greed is the most common sentiment on matched trade dates (40.3%).
- HYPE accounts for 68,005 trades, or 32.2% of all records.
- Sell and buy activity is nearly balanced: 51.38% versus 48.62%.
- Average Closed PnL is highest during Extreme Greed (67.89), although median
  Closed PnL is zero in every sentiment group.
- Fear has the largest average trade size (7,816.11 USD) and fee (1.50).
- Closed PnL has weak correlations with trade size (0.124), fee (0.084) and
  sentiment value (0.008).

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
jupyter notebook notebooks/assignment_analysis.ipynb
python -m pytest
```

Open the notebook and select **Run All** to reproduce the analysis.

## Future Improvements

Add intraday sentiment, market indicators, real-time data, an interactive
dashboard, and leakage-safe machine-learning experiments.

## License

This project is available under the MIT License
