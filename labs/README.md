# Lab sequence and entry points

1. Dataset quality report — inspect the original BME280 stream and document gaps, ranges, timestamps, and replay fitness.
2. Reproducible preprocessing — complete the chronological split, train-only scaler, and window tests in the reused original script.
3. Model and handoff parity — train with fixed seeds, beat persistence, export opset 18 ONNX, quantize for ESP32-S3, and record parity evidence.
4. QEMU replay — complete the firmware TODOs and prove real ESP-DL inference with UART JSONL evidence.

The capstone combines all four artifacts and adds failure-path evidence plus an engineering tradeoff report.

Open the guide for your current activity before changing files. Each guide names the canonical command, expected observation, evidence files, acceptance boundary, and a recovery path:

- [Lab 1 — Dataset evidence](lab-1-data-evidence.md)
- [Lab 2 — Leakage-safe preprocessing](lab-2-preprocessing.md)
- [Lab 3 — Model and handoff parity](lab-3-model-parity.md)
- [Lab 4 — ESP32-S3 QEMU replay](lab-4-qemu-replay.md)
- [Capstone — Predictive Sensor Node](capstone.md)

