"""
Module 2 — Step 2: Preprocess the time-series for LSTM training.

Pipeline:
    1. Load CSV and sort by timestamp.
    2. Split into train / validation / test using a chronological split
       (NEVER shuffle a time series — that would leak future into past).
    3. Fit a MinMax scaler on the training set only, then apply it to all
       three splits. Save the scaler parameters as JSON so the on-device
       inference code (and the C# desktop validator) can reverse the
       normalization without loading scikit-learn.
    4. Build sliding windows of length SEQ_LEN, predicting the value
       at t+1 from the window [t-SEQ_LEN+1 ... t].
    5. Save NumPy arrays for the training stage to consume.

Output files (in data/processed/):
    X_train.npy, y_train.npy
    X_val.npy,   y_val.npy
    X_test.npy,  y_test.npy
    scaler_params.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


SENSOR_COLUMNS = ["temperature_c", "humidity_pct", "pressure_hpa"]
SEQ_LEN = 24  # 24 hourly samples => one day of history per window


def chronological_split(
    df: pd.DataFrame, train_frac: float = 0.7, val_frac: float = 0.15
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # TODO(Lab 2): preserve time ordering and return disjoint train, validation,
    # and test frames. Record boundary timestamps in your evidence report.
    raise NotImplementedError("complete the chronological split")


def fit_minmax(values: np.ndarray) -> dict[str, list[float]]:
    """Return per-column min/max so we can normalize without sklearn at inference time."""
    # TODO(Lab 2): fit only on the training values.
    raise NotImplementedError("fit the train-only scaler")


def apply_minmax(values: np.ndarray, params: dict[str, list[float]]) -> np.ndarray:
    # TODO(Lab 2): apply saved parameters without refitting and handle constant
    # channels safely.
    raise NotImplementedError("apply the saved scaler")


def make_windows(series: np.ndarray, seq_len: int) -> tuple[np.ndarray, np.ndarray]:
    """
    series: shape (T, num_features), already normalized.
    returns X of shape (N, seq_len, num_features) and y of shape (N, num_features),
    where y[i] is the value immediately following X[i].
    """
    # TODO(Lab 2): predict t+1 from exactly seq_len earlier rows and reject an
    # input that is too short for one complete window.
    raise NotImplementedError("build the sliding windows")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "data" / "baseline" / "bme280_sample.csv")
    parser.add_argument("--output-dir", type=Path, default=root / "data" / "processed")
    parser.add_argument("--seq-len", type=int, default=SEQ_LEN)
    args = parser.parse_args()

    df = pd.read_csv(args.input, parse_dates=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    print(f"Loaded {len(df):,} rows from {args.input}")

    train_df, val_df, test_df = chronological_split(df)
    print(f"Split sizes — train: {len(train_df)}, val: {len(val_df)}, test: {len(test_df)}")

    train_values = train_df[SENSOR_COLUMNS].to_numpy(dtype=np.float32)
    val_values = val_df[SENSOR_COLUMNS].to_numpy(dtype=np.float32)
    test_values = test_df[SENSOR_COLUMNS].to_numpy(dtype=np.float32)

    scaler_params = fit_minmax(train_values)
    scaler_params["sensor_columns"] = SENSOR_COLUMNS
    scaler_params["seq_len"] = args.seq_len

    train_norm = apply_minmax(train_values, scaler_params)
    val_norm = apply_minmax(val_values, scaler_params)
    test_norm = apply_minmax(test_values, scaler_params)

    X_train, y_train = make_windows(train_norm, args.seq_len)
    X_val, y_val = make_windows(val_norm, args.seq_len)
    X_test, y_test = make_windows(test_norm, args.seq_len)

    print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"X_val:   {X_val.shape}, y_val:   {y_val.shape}")
    print(f"X_test:  {X_test.shape}, y_test:  {y_test.shape}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    np.save(args.output_dir / "X_train.npy", X_train)
    np.save(args.output_dir / "y_train.npy", y_train)
    np.save(args.output_dir / "X_val.npy", X_val)
    np.save(args.output_dir / "y_val.npy", y_val)
    np.save(args.output_dir / "X_test.npy", X_test)
    np.save(args.output_dir / "y_test.npy", y_test)

    with open(args.output_dir / "scaler_params.json", "w", encoding="utf-8") as f:
        json.dump(scaler_params, f, indent=2)

    print(f"Saved preprocessed arrays and scaler_params.json to {args.output_dir}")


if __name__ == "__main__":
    main()
