#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

FORBIDDEN = re.compile(r"Guru Meditation Error|panic(?:'ed)?|abort\(|assert(?:ion)? failed|Backtrace:", re.IGNORECASE)


def event_from_line(line: str) -> dict | None:
    start, end = line.find("{"), line.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        value = json.loads(line[start : end + 1])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def require_single(events: list[dict], name: str) -> tuple[int, dict]:
    found = [(index, event) for index, event in enumerate(events) if event.get("event") == name]
    if len(found) != 1:
        raise ValueError(f"expected exactly one {name} event, found {len(found)}")
    return found[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    args = parser.parse_args()
    raw = args.log.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    if FORBIDDEN.search(text):
        raise ValueError("UART contains a panic, abort, assertion, or backtrace")
    events = [event for line in text.splitlines() if (event := event_from_line(line))]
    test_index, embedded = require_single(events, "embedded_model_test")
    inference_index, inference = require_single(events, "inference")
    fault_index, fault = require_single(events, "fault_case")
    summary_index, summary = require_single(events, "course_summary")
    if not (test_index < inference_index < fault_index < summary_index):
        raise ValueError("UART events are incomplete or out of order")
    if embedded.get("passed") is not True:
        raise ValueError("embedded model test failed")
    output, expected = inference.get("output"), inference.get("expected")
    if not isinstance(output, list) or not isinstance(expected, list) or len(output) != 3 or len(expected) != 3:
        raise ValueError("inference must contain three output and expected values")
    values = [float(value) for value in output + expected]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("inference contains a non-finite value")
    errors = [abs(float(actual) - float(reference)) for actual, reference in zip(output, expected)]
    if any(error > 0.08 for error in errors):
        raise ValueError(f"replay error exceeds 0.08: {errors}")
    if inference.get("parity") is not True:
        raise ValueError("inference parity is not true")
    if fault.get("case") != "non_finite" or fault.get("rejected") is not True:
        raise ValueError("non-finite input was not rejected")
    if summary.get("unexpected_failures") != 0 or summary.get("passed") is not True:
        raise ValueError("course summary did not pass with zero unexpected failures")
    print(json.dumps({"schemaVersion": 1, "passed": True, "uartSha256": hashlib.sha256(raw).hexdigest(), "eventCount": len(events), "output": output, "expected": expected, "absoluteErrors": errors, "maxAbsoluteError": max(errors)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
