#!/usr/bin/env python3
"""Build and test the released-package shape of cad_verification.

This is consumer-owned library build/test code. CAD-CI remains responsible for
selection, dependency execution, incremental decisions and caching.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def _output_root() -> Path:
    """Return the CAD-CI-owned output directory for this item."""

    value = os.environ.get("CAD_CI_OUTPUT")
    if not value:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    return Path(value).resolve()


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None):
    """Run one build/test subprocess and echo captured output."""

    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode:
        raise RuntimeError(
            f"command failed with status {completed.returncode}: "
            + " ".join(command)
        )
    return completed


def build_package() -> None:
    """Build exactly one wheel into the declared CAD-CI output."""

    output = _output_root()
    dist = output / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    _run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--wheel-dir",
            str(dist),
            str(ROOT),
        ],
        cwd=ROOT,
    )

    wheels = tuple(sorted(dist.glob("*.whl")))
    if len(wheels) != 1:
        raise RuntimeError(
            f"expected exactly one built wheel, found {len(wheels)}"
        )
    print(f"Built package: {wheels[0].name}")


def test_package() -> None:
    """Run unit tests with imports resolved from the built wheel."""

    output = _output_root()
    wheels = tuple(sorted((output / "dist").glob("*.whl")))
    if len(wheels) != 1:
        raise RuntimeError(
            f"expected exactly one built wheel, found {len(wheels)}"
        )

    with tempfile.TemporaryDirectory(prefix="cad-verification-test-") as tmp:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(wheels[0])
        completed = _run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(ROOT / "tests"),
                "-v",
            ],
            cwd=Path(tmp),
            env=env,
        )

    combined = completed.stdout + "\n" + completed.stderr
    match = re.search(r"Ran (\d+) tests?", combined)
    count = int(match.group(1)) if match else None

    result = {
        "schema": 1,
        "status": "pass",
        "package": wheels[0].name,
        "tests": count,
    }
    (output / "test-results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Tests passed: {count if count is not None else 'count unavailable'}")


def main() -> int:
    """Dispatch the explicit library build or test action."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "test"))
    args = parser.parse_args()

    if args.action == "build":
        build_package()
    else:
        test_package()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
