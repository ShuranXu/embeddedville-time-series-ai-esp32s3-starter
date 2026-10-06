# Lab 4 — ESP32-S3 QEMU replay

Run `make ready`, then `make firmware` and `make qemu`. Work in `firmware/main/app_main.cpp` and use the supplied runner scripts.

Expected first observation: ESP-IDF boots in the pinned ESP32-S3 QEMU environment, verifies the embedded model hash, and emits JSONL records for recorded vectors. Run valid, gap, non-finite, out-of-range, and truncated suites, then `make evidence`.

If QEMU stops or disconnects, keep the UART log, stop the runner, and restart the same suite. This lab proves modeled firmware behavior only; it does not prove I²C, electrical behavior, energy, radio, or wall-clock timing on physical hardware.
