# Lab 3 — Model and handoff parity

Run `make ready`, then `make train` and `make export`. Work in `src/03_train_lstm.py`, `src/04_export_onnx.py`, `src/05_evaluate_onnx.py`, and `src/06_quantize_espdl.py`.

Expected first observation: deterministic training emits a best-validation checkpoint and sensor-unit metrics. Prove persistence, PyTorch-to-ONNX, and quantized ESP-DL parity against one locked checkpoint and scaler. The release ONNX shape is `1×24×3`, opset 18.

If conversion fails, retain the checkpoint and logs. Re-run `make ready` before rebuilding the container; do not rename an ONNX file to `.espdl` or substitute a different checkpoint.
