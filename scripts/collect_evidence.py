from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = [
    "data/baseline/bme280_sample.csv",
    "models/release/sensor_lstm_opset18.onnx",
    "models/release/sensor_lstm_c_w8a16.espdl",
    "outputs/release/qemu-uart.log",
]
records = {}
for relative in paths:
    path = ROOT / relative
    if path.exists():
        records[relative] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
out = ROOT / "outputs" / "release" / "evidence-manifest.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"schemaVersion": 2, "courseId": "time-series-ai-esp32s3", "notice": "Convenience evidence only; protected evaluation rebuilds and ignores submitted generated evidence.", "artifacts": records}, indent=2) + "\n")
print(out)

