"""Download an exact Space revision and verify hashes and preserved history."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
REPO_ID = "DineshAI/nbU2LNYdZN"
PROTECTED_MANIFEST = ROOT / ".openresearch" / "protected" / "judged_space_manifest.sha256"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        result[relative] = digest
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    destination = Path(args.output).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise RuntimeError("Output directory must be fresh and empty")
    destination.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        REPO_ID,
        repo_type="space",
        revision=args.revision,
        local_dir=destination,
        force_download=True,
        max_workers=8,
    )
    api = HfApi()
    exact = api.repo_info(REPO_ID, repo_type="space", revision=args.revision).sha
    if exact != args.revision:
        raise RuntimeError(f"Downloaded revision mismatch: {exact}")
    upload_hashes = parse_manifest(CANDIDATE / "evidence" / "upload_manifest.sha256")
    mismatches = [
        relative
        for relative, digest in upload_hashes.items()
        if not (destination / relative).is_file()
        or sha256(destination / relative) != digest
    ]
    protected = parse_manifest(PROTECTED_MANIFEST)
    missing_old = [
        relative for relative in protected if not (destination / relative).is_file()
    ]
    historical = ["pages/overview/page.md", "pages/verify/page.md"]
    historical_mismatches = [
        relative
        for relative in historical
        if sha256(destination / relative) != protected[relative]
    ]
    report = {
        "space_id": REPO_ID,
        "revision": exact,
        "download_directory": str(destination),
        "uploaded_hashes_checked": len(upload_hashes),
        "upload_hash_mismatches": mismatches,
        "old_file_set_present": not missing_old,
        "missing_old_paths": missing_old,
        "historical_page_hash_mismatches": historical_mismatches,
        "passed": not mismatches and not missing_old and not historical_mismatches,
    }
    (destination / "postpublication_verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
