from __future__ import annotations

import argparse
import hashlib
import json
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MAX_FILES = 200
MAX_BYTES = 64 * 1024 * 1024
FIXED_FILES = {
    "course-version.json": "configuration",
    "submission/evidence.md": "evidence",
    "data/baseline/bme280_sample.csv": "dataset",
}
TREES = {
    "src": {".py": "source"},
    "firmware": {
        ".cpp": "source",
        ".c": "source",
        ".h": "source",
        ".hpp": "source",
        ".txt": "configuration",
        ".yml": "configuration",
        ".yaml": "configuration",
        ".defaults": "configuration",
        ".csv": "configuration",
    },
    "models/release": {".pt": "checkpoint", ".pth": "checkpoint"},
    "data/model-inputs": {".npy": "model-input", ".npz": "model-input", ".json": "model-input", ".csv": "model-input"},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def checked_file(relative: str, role: str) -> tuple[Path, str, str]:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe submission path: {relative}")
    path = ROOT.joinpath(*pure.parts)
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise ValueError(f"submission entry must be a regular file: {relative}")
    return path, pure.as_posix(), role


def collect() -> list[tuple[Path, str, str]]:
    selected = []
    for relative, role in FIXED_FILES.items():
        if (ROOT / relative).is_file():
            selected.append(checked_file(relative, role))
    for tree, suffix_roles in TREES.items():
        base = ROOT / tree
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"links are prohibited in submissions: {path.relative_to(ROOT)}")
            if path.is_file() and path.suffix.lower() in suffix_roles:
                relative = path.relative_to(ROOT).as_posix()
                selected.append(checked_file(relative, suffix_roles[path.suffix.lower()]))
    deduplicated = {relative: (path, relative, role) for path, relative, role in selected}
    files = [deduplicated[key] for key in sorted(deduplicated)]
    if len(files) > MAX_FILES:
        raise ValueError(f"submission contains {len(files)} files; maximum is {MAX_FILES}")
    total = sum(path.stat().st_size for path, _, _ in files)
    if total > MAX_BYTES:
        raise ValueError(f"submission payload is {total} bytes; maximum is {MAX_BYTES}")
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("item_id")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract = json.loads((ROOT / "course-version.json").read_text(encoding="utf-8"))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    files = collect()
    manifest = {
        "schemaVersion": 2,
        "courseId": contract["courseId"],
        "itemId": args.item_id,
        "courseContract": contract["courseContract"],
        "evaluatorContract": contract["evaluatorContract"],
        "starter": {"tag": contract["starterTag"], "commit": commit},
        "files": [
            {"path": relative, "sha256": sha256(path), "role": role}
            for path, relative, role in files
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED, strict_timestamps=True) as archive:
        archive.writestr("submission-manifest.json", json.dumps(manifest, indent=2) + "\n")
        for path, relative, _ in files:
            archive.write(path, relative)
    if args.output.stat().st_size > MAX_BYTES:
        args.output.unlink(missing_ok=True)
        raise ValueError("compressed archive exceeds the 64-MiB boundary")
    print(args.output)


if __name__ == "__main__":
    main()
