"""
Module 2 — Step 0: Generate a synthetic BME280-like dataset.

The real course code will read a CSV logged from a BME280 sensor attached to
the ESP32-S3. Until students have hardware in hand, this script produces a
realistic stand-in dataset so the rest of the pipeline (preprocessing,
training, ONNX export, inference) can be developed and tested end-to-end.

Output:
    data/bme280_sample.csv with columns:
        timestamp, temperature_c, humidity_pct, pressure_hpa

Signal model (deterministic given the seed):
    - temperature: daily sinusoidal cycle around 22 degC + small drift + noise
    - humidity:    anti-correlated with temperature (warm air holds more H2O)
    - pressure:    slow weekly variation around 1013 hPa + small noise
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate(
    n_hours: int = 24 * 90,
    start: str = "2025-01-01 00:00:00",
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(n_hours, dtype=float)

    # Daily cycle (24h period). Hour-of-day phase aligned so peak temp is mid-afternoon.
    daily = np.sin(2 * np.pi * (t - 14) / 24.0)

    # Weekly cycle for pressure.
    weekly = np.sin(2 * np.pi * t / (24 * 7))

    # Slow seasonal drift across the window.
    drift = np.linspace(0.0, 1.5, n_hours)

    temperature = 22.0 + 3.0 * daily + drift + rng.normal(0, 0.35, n_hours)
    humidity = 50.0 - 10.0 * daily - 0.5 * drift + rng.normal(0, 1.8, n_hours)
    humidity = np.clip(humidity, 10.0, 95.0)
    pressure = 1013.0 + 2.5 * weekly + rng.normal(0, 0.25, n_hours)

    timestamps = pd.date_range(start=start, periods=n_hours, freq="h")
    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "temperature_c": np.round(temperature, 2),
            "humidity_pct": np.round(humidity, 2),
            "pressure_hpa": np.round(pressure, 2),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hours", type=int, default=24 * 90, help="Number of hourly samples to generate.")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "bme280_sample.csv",
        help="Output CSV path.",
    )
    args = parser.parse_args()

    df = generate(n_hours=args.hours, seed=args.seed)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)

    print(f"Wrote {len(df):,} rows to {args.output}")
    print(df.head())
    print("...")
    print(df.tail())


if __name__ == "__main__":
    main()
