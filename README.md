# Stock Portfolio Tracker (CodeAlpha Task 2)

A simple CLI stock portfolio tracker that calculates total investment value using **hardcoded stock prices**.

## Features

- Enter stock symbols and quantities interactively
- Uses a hardcoded price dictionary (easy to edit)
- Displays a clear portfolio summary and **total investment value**
- Optional export to **TXT** or **CSV**

## Requirements

- Python 3.10+ (recommended)

## How to Run (macOS)

From the project folder:

```bash
python3 main.py
```

## How It Works

1. The script shows available stock symbols and their prices.
2. You enter:
   - **Stock symbol** (e.g., `AAPL`)
   - **Quantity** (e.g., `10`)
3. Type `done` to finish.
4. The program prints the portfolio table and total.
5. Optionally save the results to `.txt` or `.csv`.

## Available Stocks (Hardcoded)

Defined in `main.py` as `STOCK_PRICES`.

Example:

- `AAPL`: 180
- `TSLA`: 250
- `GOOGL`: 175
- `AMZN`: 185
- `MSFT`: 420

You can add/remove symbols by editing the `STOCK_PRICES` dictionary.

## Output Files

### CSV format

When saving as CSV, the file includes:

- A `saved_at` timestamp row
- A table with columns: `symbol, quantity, price, value`
- A final `TOTAL` row

Example (`stok.csv`):

```csv
saved_at,2026-05-24T19:54:04

symbol,quantity,price,value
AAPL,10.0,180.0,1800.0
TSLA,10.0,250.0,2500.0

TOTAL,,,4300.0
```

### TXT format

A human-readable table and total.

## Notes

- Prices are static/hardcoded (this project does not fetch live market prices).
- Quantities accept decimal values (e.g., `1.5`).
