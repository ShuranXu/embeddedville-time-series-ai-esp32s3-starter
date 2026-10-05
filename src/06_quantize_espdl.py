"""Lab 3B ESP-DL quantization scaffold."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    # TODO(Lab 3B): use esp-ppq at the commit pinned by course-version.json,
    # calibrate from training windows, target esp32s3 w8a8, export test values,
    # and record ONNX/.espdl/test-vector SHA-256 values.
    raise NotImplementedError("complete ESP-DL quantization")

if __name__ == "__main__":
    main()

