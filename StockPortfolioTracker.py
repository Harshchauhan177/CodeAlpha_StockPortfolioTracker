# Stock Portfolio Tracker (CodeAlpha Task 2)
# - User inputs stock symbols and quantities
# - Uses hardcoded prices
# - Calculates total investment value
# - Optionally saves results to .txt or .csv

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


# Hardcoded stock prices (USD)
STOCK_PRICES: dict[str, float] = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 175.0,
    "AMZN": 185.0,
    "MSFT": 420.0,
}


@dataclass(frozen=True)
class Holding:
    symbol: str
    quantity: float
    price: float

    @property
    def value(self) -> float:
        return self.quantity * self.price


def _money(x: float) -> str:
    return f"${x:,.2f}"


def _read_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")


def _read_positive_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive number.")


def collect_holdings(prices: dict[str, float]) -> list[Holding]:
    print("\nAvailable stocks/prices:")
    for sym, p in prices.items():
        print(f"  {sym:<6} {_money(p)}")

    print("\nEnter your portfolio. Type 'done' when finished.\n")

    holdings: list[Holding] = []
    while True:
        symbol = _read_non_empty("Stock symbol (e.g., AAPL) or 'done': ").upper()
        if symbol in {"DONE", "EXIT", "QUIT"}:
            break

        if symbol not in prices:
            print("Unknown symbol. Choose from:", ", ".join(sorted(prices.keys())))
            continue

        qty = _read_positive_float(f"Quantity for {symbol}: ")
        holdings.append(Holding(symbol=symbol, quantity=qty, price=prices[symbol]))
        print(f"Added: {symbol} x {qty} @ {_money(prices[symbol])}\n")

    return holdings


def print_summary(holdings: list[Holding]) -> float:
    if not holdings:
        print("\nNo holdings entered.")
        return 0.0

    print("\nPortfolio Summary")
    print("-" * 60)
    print(f"{'SYMBOL':<10}{'QTY':>10}{'PRICE':>15}{'VALUE':>15}")
    print("-" * 60)

    total = 0.0
    for h in holdings:
        total += h.value
        print(f"{h.symbol:<10}{h.quantity:>10.4g}{_money(h.price):>15}{_money(h.value):>15}")

    print("-" * 60)
    print(f"{'TOTAL':<35}{_money(total):>25}")
    return total


def save_txt(path: Path, holdings: list[Holding], total: float) -> None:
    lines: list[str] = []
    lines.append(f"Saved at: {datetime.now().isoformat(timespec='seconds')}\n")
    lines.append("Portfolio Summary\n")
    lines.append(f"{'SYMBOL':<10}{'QTY':>10}{'PRICE':>15}{'VALUE':>15}\n")
    for h in holdings:
        lines.append(
            f"{h.symbol:<10}{h.quantity:>10.4g}{_money(h.price):>15}{_money(h.value):>15}\n"
        )
    lines.append(f"\nTOTAL: {_money(total)}\n")
    path.write_text("".join(lines), encoding="utf-8")


def save_csv(path: Path, holdings: list[Holding], total: float) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["saved_at", datetime.now().isoformat(timespec="seconds")])
        writer.writerow([])
        writer.writerow(["symbol", "quantity", "price", "value"])
        for h in holdings:
            writer.writerow([h.symbol, h.quantity, h.price, h.value])
        writer.writerow([])
        writer.writerow(["TOTAL", "", "", total])


def maybe_save(holdings: list[Holding], total: float) -> None:
    if not holdings:
        return

    choice = input("\nSave result to a file? (n/txt/csv): ").strip().lower()
    if choice in {"n", "no", ""}:
        return

    default_name = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if choice in {"txt", "t"}:
        file_name = input(f"Filename (default: {default_name}.txt): ").strip() or f"{default_name}.txt"
        path = Path(file_name)
        if path.suffix.lower() != ".txt":
            path = path.with_suffix(".txt")
        save_txt(path, holdings, total)
        print(f"Saved to: {path.resolve()}")
        return

    if choice in {"csv", "c"}:
        file_name = input(f"Filename (default: {default_name}.csv): ").strip() or f"{default_name}.csv"
        path = Path(file_name)
        if path.suffix.lower() != ".csv":
            path = path.with_suffix(".csv")
        save_csv(path, holdings, total)
        print(f"Saved to: {path.resolve()}")
        return

    print("Not saved (unrecognized option).")


def main() -> None:
    print("Stock Portfolio Tracker")
    print("=" * 24)

    holdings = collect_holdings(STOCK_PRICES)
    total = print_summary(holdings)
    maybe_save(holdings, total)


if __name__ == "__main__":
    main()
