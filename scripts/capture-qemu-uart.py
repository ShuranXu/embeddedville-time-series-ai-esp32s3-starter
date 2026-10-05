#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path


def event_from_line(line: str) -> dict | None:
    start, end = line.find("{"), line.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        value = json.loads(line[start : end + 1])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def stop_group(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--deadline", type=float, default=90.0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a QEMU command is required after --")
    args.log.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, start_new_session=True)
    assert process.stdout is not None
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + args.deadline
    passed_summary = False
    with args.log.open("w", encoding="utf-8", newline="") as log:
        while time.monotonic() < deadline:
            ready = selector.select(timeout=min(1.0, max(0.0, deadline - time.monotonic())))
            if not ready:
                if process.poll() is not None:
                    break
                continue
            line = process.stdout.readline()
            if line == "":
                if process.poll() is not None:
                    break
                continue
            sys.stdout.write(line)
            sys.stdout.flush()
            log.write(line)
            log.flush()
            event = event_from_line(line)
            if event and event.get("event") == "course_summary" and event.get("passed") is True and event.get("unexpected_failures") == 0:
                passed_summary = True
                break
    stop_group(process)
    if not passed_summary:
        print("QEMU deadline/process exit occurred before a complete passing summary.", file=sys.stderr)
        return 124
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
