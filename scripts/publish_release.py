#!/usr/bin/env python3
"""Publish the declared library release after the exact main commit passed CI."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def release_version(root: Path = ROOT) -> str:
    """Return the release version after all repository version sources agree."""

    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not _VERSION.fullmatch(version):
        raise ValueError(f"VERSION is not a release version: {version}")

    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    if f'version = "{version}"' not in pyproject:
        raise ValueError("VERSION and pyproject.toml do not match")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if re.search(
        rf"^## {re.escape(version)}(?:\s|$)",
        changelog,
        re.MULTILINE,
    ) is None:
        raise ValueError(f"CHANGELOG.md has no {version} release section")
    return version


def version_changed(root: Path = ROOT) -> bool:
    """Return whether VERSION changed in the current Git commit."""

    parent = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD^"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if parent.returncode != 0:
        return True

    changed = subprocess.run(
        ["git", "diff", "--quiet", "HEAD^", "HEAD", "--", "VERSION"],
        cwd=root,
        check=False,
    )
    if changed.returncode == 0:
        return False
    if changed.returncode == 1:
        return True
    raise ValueError("could not determine whether VERSION changed")


def _request(
    url: str,
    token: str,
    *,
    method: str = "GET",
    data: dict | None = None,
):
    """Send one authenticated GitHub REST request and decode JSON."""

    payload = None if data is None else json.dumps(data).encode("utf-8")
    request = Request(
        url,
        data=payload,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def publish(repository: str, sha: str, token: str, root: Path = ROOT) -> str:
    """Publish only when VERSION changed in the exact tested main commit."""

    if not version_changed(root):
        return "VERSION unchanged; no release"

    version = release_version(root)
    tag = f"v{version}"
    base = f"https://api.github.com/repos/{repository}"

    try:
        existing = _request(f"{base}/releases/tags/{tag}", token)
    except HTTPError as exc:
        if exc.code != 404:
            raise
    else:
        target = str(existing.get("target_commitish", ""))
        if target and target != sha:
            raise ValueError(
                f"{tag} already points to {target}, expected tested main {sha}"
            )
        return f"release already exists: {tag}"

    _request(
        f"{base}/releases",
        token,
        method="POST",
        data={
            "tag_name": tag,
            "target_commitish": sha,
            "name": f"lib.py.cad.verfication {version}",
            "body": f"lib.py.cad.verfication {version}",
            "draft": False,
            "prerelease": False,
        },
    )
    return f"published release: {tag} at {sha}"


def main() -> int:
    """Publish using the repository, SHA and token supplied by GitHub Actions."""

    repository = os.environ.get("GITHUB_REPOSITORY", "")
    sha = os.environ.get("GITHUB_SHA", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repository or not sha or not token:
        print(
            "ERROR: GITHUB_REPOSITORY, GITHUB_SHA and GITHUB_TOKEN are required",
            file=sys.stderr,
        )
        return 2
    try:
        print(publish(repository, sha, token))
    except (ValueError, HTTPError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
