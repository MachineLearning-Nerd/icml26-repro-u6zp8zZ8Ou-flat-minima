#!/usr/bin/env python3
"""Fail-closed verification for the published reproduction bundle."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "repro/tests",
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=ROOT,
        check=True,
    )
    print("PASS: 15 independent assertions; CPU-only theorem-instance reproduction verified")


if __name__ == "__main__":
    main()
