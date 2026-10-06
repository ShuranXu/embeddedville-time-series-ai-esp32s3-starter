# Lab 1 — Dataset evidence

Run `make ready`, then `make explore`. Work in `src/00_generate_sample_data.py` and `src/01_explore_data.py`.

Expected first observation: the seed-42 CSV has hourly timestamps and the generated plot shows temperature, humidity, and pressure as separate channels. Complete the duplicate, cadence-gap, non-finite, range, persistence, and fault-injection checks described on the course lab page. Store results under `evidence/` and finish with `make evidence`.

If the baseline CSV was changed, preserve your reports and regenerate the source with `python src/00_generate_sample_data.py --seed 42`. Do not replace an existing report until you have saved the learner-authored copy.
