from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = ["course-version.json", "outputs/release/evidence-manifest.json", "outputs/release/05_metrics.txt", "outputs/release/parity.json", "outputs/release/qemu-uart.log", "submission/evidence.md"]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("item_id")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    files = [ROOT / name for name in ALLOWED if (ROOT / name).is_file()]
    manifest = {"schemaVersion": 1, "courseId": "time-series-ai-esp32s3", "itemId": args.item_id, "starterTag": "starter-v1.0.0", "files": [{"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in files]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("submission-manifest.json", json.dumps(manifest, indent=2) + "\n")
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    print(args.output)

if __name__ == "__main__":
    main()

