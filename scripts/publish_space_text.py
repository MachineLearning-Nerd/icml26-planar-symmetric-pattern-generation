"""Publish the audited text-only candidate to the existing Hugging Face Space."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi


ROOT = Path(__file__).resolve().parents[1]
SPACE = ROOT / "space_candidate"
ALLOWLIST = SPACE / "evidence" / "upload_allowlist.txt"
MANIFEST = SPACE / "evidence" / "upload_manifest.sha256"
REPO_ID = "DineshAI/nbU2LNYdZN"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-parent", required=True)
    args = parser.parse_args()
    api = HfApi()
    remote = api.repo_info(REPO_ID, repo_type="space")
    if remote.sha != args.expected_parent:
        raise RuntimeError(
            f"Space head changed: expected {args.expected_parent}, observed {remote.sha}"
        )
    paths = ALLOWLIST.read_text(encoding="utf-8").splitlines()
    if len(paths) != len(set(paths)):
        raise RuntimeError("Upload allowlist contains duplicates")
    expected_hashes = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        expected_hashes[relative] = digest
    for relative in paths:
        path = SPACE / relative
        if not path.is_file():
            raise RuntimeError(f"Allowlisted file is missing: {relative}")
        data = path.read_bytes()
        data.decode("utf-8")
        if b"\x00" in data:
            raise RuntimeError(f"Non-text payload rejected: {relative}")
        if relative in expected_hashes and sha256(path) != expected_hashes[relative]:
            raise RuntimeError(f"Manifest mismatch: {relative}")
    operations = [
        CommitOperationAdd(path_in_repo=relative, path_or_fileobj=SPACE / relative)
        for relative in paths
    ]
    result = api.create_commit(
        repo_id=REPO_ID,
        repo_type="space",
        revision="main",
        parent_commit=args.expected_parent,
        operations=operations,
        commit_message="Publish claim-by-claim CPU reproduction evidence",
        commit_description=(
            "Additive text-only release: Claims 1-5 VERIFIED; Claim 6 BLOCKED "
            "at one versus 1,000 samples per group. Historical evidence preserved."
        ),
        num_threads=8,
    )
    print(
        json.dumps(
            {
                "space_id": REPO_ID,
                "parent_revision": args.expected_parent,
                "published_revision": result.oid,
                "uploaded_text_paths": len(paths),
                "commit_url": result.commit_url,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
