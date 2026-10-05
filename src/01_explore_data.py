"""
Module 2 — Step 1: Explore the time-series dataset.

Goals for students:
    1. Open a CSV with a timestamp column and read it correctly.
    2. Inspect basic shape, missing values, and value ranges.
    3. Plot each sensor channel to build intuition about the signal:
       periodicity, range, noise level, sensor drift.

This is a feel-the-data step — no machine learning yet. Run it before
preprocessing so you know what your model has to learn.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


SENSOR_COLUMNS = ["temperature_c", "humidity_pct", "pressure_hpa"]


def load(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


def summarize(df: pd.DataFrame) -> None:
    print(f"Rows:         {len(df):,}")
    print(f"Time range:   {df['timestamp'].min()}  →  {df['timestamp'].max()}")
    print(f"Columns:      {list(df.columns)}")
    print()
    print("Missing values per column:")
    print(df.isna().sum().to_string())
    print()
    print("Per-channel statistics:")
    print(df[SENSOR_COLUMNS].describe().round(3).to_string())


def plot_channels(df: pd.DataFrame, save_to: Path | None = None) -> None:
    fig, axes = plt.subplots(len(SENSOR_COLUMNS), 1, figsize=(11, 7), sharex=True)
    for ax, col in zip(axes, SENSOR_COLUMNS):
        ax.plot(df["timestamp"], df[col], linewidth=0.8)
        ax.set_ylabel(col)
        ax.grid(True, alpha=0.3)
    axes[-1].set_xlabel("timestamp")
    fig.suptitle("BME280 channels over time")
    fig.tight_layout()

    if save_to is not None:
        save_to.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_to, dpi=120)
        print(f"Saved plot to {save_to}")
    else:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "bme280_sample.csv",
    )
    parser.add_argument(
        "--save-plot",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "outputs" / "01_channels.png",
        help="If set, write the figure instead of opening a window.",
    )
    parser.add_argument("--no-save", action="store_true", help="Show the plot interactively instead of saving.")
    args = parser.parse_args()

    df = load(args.input)
    summarize(df)
    plot_channels(df, save_to=None if args.no_save else args.save_plot)


if __name__ == "__main__":
    main()
