# Lab 2 — Leakage-safe preprocessing

Run `make ready`, then `make preprocess`. Work in `src/02_preprocessing.py`.

Expected first observation: chronological train, validation, and test boundaries are printed before scaling. Complete the train-only scaler, `[N, 24, 3]` window, independent parity, zero-span, and short-series checks described on the course lab page. Store versioned outputs under `evidence/`.

If arrays no longer match the baseline, save learner work, remove only generated files named by the lab page, and rerun preprocessing. Never overwrite the source CSV to repair a generated-array mismatch.
