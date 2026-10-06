# Time-Series AI on ESP32-S3 — learner starter

This is the published, solution-free workspace for EmbeddedVille course `time-series-ai-esp32s3`. The pinned W8A16 reference build passes the protected evaluator and ESP32-S3 QEMU replay gate.

This is the solution-free workspace for EmbeddedVille course `time-series-ai-esp32s3`. It preserves the original BME280 dataset, baseline arrays, checkpoint, ONNX model, metrics, and plots while turning the original scripts into progressive exercises.

## Start or resume in Codespaces

1. Launch the exact course release from the link on the EmbeddedVille lab page. The link may resume an existing matching Codespace, so check `make ready` before doing new work.
2. Wait for the pinned dev container to finish, then run `make ready`.
3. If `make ready` reports a version mismatch, do not force-pull or replace your branch. Commit or download learner-created files, create a fresh Codespace from the course link, and copy only those files into the fresh workspace.
4. Closing the browser tab does not necessarily stop the Codespace. Stop compute from the Codespaces page when idle. A stopped Codespace normally preserves saved files, but terminal screen contents are not durable evidence.
5. Delete a Codespace only after pushing or downloading your work. Deletion or retention expiry can remove unpushed files.
6. Codespaces requires a GitHub account, repository access, a supported browser, internet access, and available quota. Usage can incur compute and storage charges after included quotas; review GitHub billing before launch.

The dev container exposes no public ports and asks only for access to this repository. A rebuild can replace container-installed state, while files saved under `/workspaces` normally remain. Preserve your work before rebuilding or creating a replacement.

GitHub's current lifecycle reference: <https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle>

## Choose the lab you are doing

- [Lab 1 — Dataset evidence](labs/lab-1-data-evidence.md)
- [Lab 2 — Leakage-safe preprocessing](labs/lab-2-preprocessing.md)
- [Lab 3 — Model and handoff parity](labs/lab-3-model-parity.md)
- [Lab 4 — ESP32-S3 QEMU replay](labs/lab-4-qemu-replay.md)
- [Capstone — Predictive Sensor Node](labs/capstone.md)

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

The original ONNX model is a comparison artifact. It does not execute unchanged on the MCU. The release path is PyTorch → corrected opset 18 ONNX → W8A16 ESP-DL `.espdl` → generic C/reference ESP-DL kernels → real ESP-IDF firmware in ESP32-S3 QEMU. The ESP32-S3 PIE W8A8 build remains a diagnostic/optional-hardware profile, not the authoritative simulator profile.

Physical ESP32-S3/BME280 hardware is optional enrichment. QEMU does not validate BME280 I²C, electrical behavior, radio, energy, or physical real-time latency.

