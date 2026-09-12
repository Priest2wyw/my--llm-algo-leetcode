#!/usr/bin/env python3
"""Download and validate the learning material listed in the task manifest."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPOSITORY_ROOT / "downloads" / "task_manifest.json"
REQUIRED_FIELDS = {"task", "kind", "url", "path"}
VALID_TASKS = {"task0", "task1"}
VALID_KINDS = {"notebook", "reference"}


def load_manifest(path: Path | str) -> list[dict[str, str]]:
    """Load and structurally validate a task download manifest."""
    manifest_path = Path(path)
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest {manifest_path}: {exc}") from exc

    if not isinstance(data, list) or not data:
        raise ValueError("manifest must be a non-empty JSON list")

    entries: list[dict[str, str]] = []
    paths: set[str] = set()
    for index, entry in enumerate(data, start=1):
        if not isinstance(entry, dict) or set(entry) != REQUIRED_FIELDS:
            raise ValueError(f"manifest entry {index} must contain exactly {sorted(REQUIRED_FIELDS)}")
        if entry["task"] not in VALID_TASKS or entry["kind"] not in VALID_KINDS:
            raise ValueError(f"manifest entry {index} has an invalid task or kind")
        if not entry["url"].startswith("https://"):
            raise ValueError(f"manifest entry {index} must use an HTTPS URL")
        relative_path = Path(entry["path"])
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"manifest entry {index} has an unsafe local path")
        if relative_path.parts[:1] != (entry["task"],):
            raise ValueError(f"manifest entry {index} path must be under its task directory")
        if entry["path"] in paths:
            raise ValueError(f"manifest contains duplicate path {entry['path']}")
        paths.add(entry["path"])
        entries.append(entry)
    return entries


def validate_notebook_bytes(data: bytes, path: Path | str) -> None:
    """Ensure bytes contain a non-empty Jupyter notebook JSON document."""
    notebook_path = Path(path)
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{notebook_path} is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("cells"), list) or not document["cells"]:
        raise ValueError(f"{notebook_path} is not a non-empty notebook")


def validate_local_file(path: Path | str, kind: str) -> None:
    """Validate a downloaded local file according to its manifest kind."""
    local_path = Path(path)
    if not local_path.is_file() or local_path.stat().st_size == 0:
        raise ValueError(f"missing or empty file: {local_path}")
    data = local_path.read_bytes()
    if kind == "notebook":
        validate_notebook_bytes(data, local_path)
    elif kind == "reference":
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"{local_path} is not valid UTF-8 text: {exc}") from exc
    else:
        raise ValueError(f"unsupported file kind {kind!r} for {local_path}")


def _destination(entry: dict[str, str]) -> Path:
    destination = (REPOSITORY_ROOT / entry["path"]).resolve()
    try:
        destination.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"manifest path escapes repository: {entry['path']}") from exc
    return destination


def download_entry(entry: dict[str, str], *, force: bool = False) -> Path:
    """Download one entry, preserving existing homework unless forced."""
    destination = _destination(entry)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        validate_local_file(destination, entry["kind"])
        return destination

    request = Request(entry["url"], headers={"User-Agent": "llm-algo-leetcode-task-downloader/1"})
    try:
        with urlopen(request, timeout=60) as response:
            data = response.read()
    except Exception as exc:
        raise RuntimeError(f"download failed for {entry['path']}: {exc}") from exc

    if entry["kind"] == "notebook":
        validate_notebook_bytes(data, destination)
    elif not data:
        raise ValueError(f"downloaded file is empty: {entry['path']}")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"downloaded file is not UTF-8 text: {entry['path']}") from exc

    temporary_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = temporary.name
            temporary.write(data)
        os.replace(temporary_path, destination)
    finally:
        if temporary_path and Path(temporary_path).exists():
            Path(temporary_path).unlink()
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true", help="validate existing files without downloading")
    parser.add_argument("--force", action="store_true", help="replace existing local files")
    args = parser.parse_args()

    entries = load_manifest(args.manifest)
    for entry in entries:
        destination = _destination(entry)
        if args.check:
            validate_local_file(destination, entry["kind"])
            print(f"OK   {entry['path']}")
        else:
            existed = destination.exists() and not args.force
            download_entry(entry, force=args.force)
            print(f"SKIP {entry['path']} (already exists)" if existed else f"GET  {entry['path']}")
    print(f"Validated {len(entries)} manifest entries") if args.check else print(f"Downloaded {len(entries)} manifest entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
