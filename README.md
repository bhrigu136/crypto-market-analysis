# Crypto Market Analysis

## Overview

This project examines the relationship between Bitcoin market sentiment and
historical trader performance. It is structured as a reproducible data analysis
project, with separate areas for raw data, reusable Python code, notebooks,
tests, generated plots, and written reports.

## Project Structure

```text
crypto-market-analysis/
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|-- plots/
|-- reports/
|-- src/
|   |-- analysis.py
|   |-- config.py
|   |-- loader.py
|   |-- preprocessing.py
|   |-- utils.py
|   `-- visualization.py
|-- tests/
|-- .gitignore
|-- LICENSE
|-- README.md
`-- requirements.txt
```

## Installation

Python 3.10 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Datasets

The analysis will use two datasets:

- Bitcoin Fear & Greed Index data
- Hyperliquid historical trader data

Dataset loading, schema details, and data-quality notes will be documented in a
later phase. Raw and processed files are kept in separate directories to
preserve reproducibility.

## Workflow

The planned workflow covers data loading, validation, cleaning, merging,
exploratory analysis, visualization, statistical analysis, and interpretation.
Reusable logic will live in `src/`, while notebooks will present the analysis
in a readable sequence.

## Results

Results will be added after the datasets have been validated and analyzed. No
findings are reported at this initialization stage.

## Future Improvements

Potential extensions will be evaluated after the core exploratory analysis is
complete.


