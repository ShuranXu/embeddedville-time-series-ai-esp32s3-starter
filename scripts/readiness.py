from __future__ import annotations
import hashlib, json, platform, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
contract = json.loads((ROOT / "course-version.json").read_text())
required = [contract["dataset"], contract["originalOnnx"], "src/02_preprocessing.py", "firmware/main/app_main.cpp"]
missing = [path for path in required if not (ROOT / path).exists()]
if missing:
    raise SystemExit(f"missing required starter files: {missing}")
architecture = platform.machine().lower()
if architecture not in {"x86_64", "aarch64", "arm64"}:
    raise SystemExit(f"unsupported course host architecture: {architecture}")
head = subprocess.run(["git", "describe", "--tags", "--exact-match"], cwd=ROOT, text=True, capture_output=True)
commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
idf = ROOT / ".tooling" / "esp-idf"
if not idf.is_dir():
    raise SystemExit("pinned ESP-IDF checkout is missing; rerun scripts/bootstrap.sh")
idf_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=idf, text=True, capture_output=True, check=True).stdout.strip()
if idf_head != contract["espIdfCommit"]:
    raise SystemExit(f"ESP-IDF commit drift: expected {contract['espIdfCommit']}, got {idf_head}")
qemu = subprocess.run([str(ROOT / "scripts" / "install-pinned-qemu.sh")], cwd=ROOT, text=True, capture_output=True)
if qemu.returncode:
    raise SystemExit(qemu.stderr.strip() or "pinned QEMU readiness failed")
print(json.dumps({"courseId": contract["courseId"], "python": platform.python_version(), "architecture": architecture, "tag": head.stdout.strip() or "untagged-development", "commit": commit, "espIdfCommit": idf_head, "qemu": qemu.stdout.strip(), "datasetSha256": hashlib.sha256((ROOT / contract["dataset"]).read_bytes()).hexdigest()}, indent=2))
if head.returncode == 0 and head.stdout.strip() != contract["starterTag"]:
    raise SystemExit("stale starter tag; recreate the workspace from course-version.json")

