# Time-Series AI on ESP32-S3 — learner starter

> **Draft workspace:** the current ESP32-S3-targeted ESP-DL LSTM does not yet pass the required QEMU parity gate. This repository is versioned for review, but the paid course must not be promoted until that gate passes.

This is the solution-free workspace for EmbeddedVille course `time-series-ai-esp32s3`. It preserves the original BME280 dataset, baseline arrays, checkpoint, ONNX model, metrics, and plots while turning the original scripts into progressive exercises.

## Start in Codespaces

1. Open this repository at the immutable course tag named in `course-version.json` and choose **Code → Codespaces → Create codespace**.
2. Wait for the pinned dev container to finish, then run `make ready`.
3. Codespaces keeps files under `/workspaces` when the browser closes. Use **Stop codespace** when idle; a stopped codespace can be resumed from github.com/codespaces.
4. Delete a codespace only after pushing or downloading your evidence. Deletion is recoverable only during GitHub's retention window; uncommitted files are not a substitute for a backup.
5. Compute and storage can incur charges after included quotas. Stop idle environments and review your GitHub billing page.
6. If the course reports a stale workspace, commit or download learner work, create a fresh codespace from the exact tag in `course-version.json`, then copy only learner-authored files back.

GitHub's current lifecycle reference: <https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle>

## Deterministic commands

```bash
make ready        # environment and immutable-version checks
make explore      # baseline dataset report and plot
make preprocess   # Lab 2 scaffold
make train        # Lab 3A scaffold
make export       # Lab 3B ONNX/ESP-DL scaffold
make firmware     # ESP-IDF build after Lab 4 TODOs are complete
make qemu         # real ESP32-S3 QEMU replay, never simulated inference
make evidence     # collect hashes, metrics, parity, and UART records
make package      # build a manifest-bound private submission ZIP
```

The original ONNX model is a comparison artifact. It does not execute unchanged on the MCU. The release path is PyTorch → corrected opset 18 ONNX → quantized ESP-DL `.espdl` → real ESP-IDF firmware in ESP32-S3 QEMU.

Physical ESP32-S3/BME280 hardware is optional enrichment. QEMU does not validate BME280 I²C, electrical behavior, radio, energy, or physical real-time latency.

