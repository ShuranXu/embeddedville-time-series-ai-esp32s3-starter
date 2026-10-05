from __future__ import annotations
import hashlib, json, platform, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
contract = json.loads((ROOT / "course-version.json").read_text())
required = [contract["dataset"], contract["originalOnnx"], "src/02_preprocessing.py", "firmware/main/app_main.cpp"]
missing = [path for path in required if not (ROOT / path).exists()]
if missing:
    raise SystemExit(f"missing required starter files: {missing}")
head = subprocess.run(["git", "describe", "--tags", "--exact-match"], cwd=ROOT, text=True, capture_output=True)
print(json.dumps({"courseId": contract["courseId"], "python": platform.python_version(), "tag": head.stdout.strip() or "untagged-development", "datasetSha256": hashlib.sha256((ROOT / contract["dataset"]).read_bytes()).hexdigest()}, indent=2))
if head.returncode == 0 and head.stdout.strip() != contract["starterTag"]:
    raise SystemExit("stale starter tag; recreate the workspace from course-version.json")

