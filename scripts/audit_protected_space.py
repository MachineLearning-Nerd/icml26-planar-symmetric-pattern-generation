"""Prove the judged Space file set remains present in the additive candidate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
MANIFEST = ROOT / ".openresearch" / "protected" / "judged_space_manifest.sha256"
REPORT = CANDIDATE / "evidence" / "protected_subset_report.json"
ALLOWED_UPDATED_ENTRYPOINTS = {"README.md", "logbook.json", "pages/index.md"}
PROTECTED_PAGES = {"pages/overview/page.md", "pages/verify/page.md"}


def sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    expected = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        expected[relative] = digest

    missing = sorted(relative for relative in expected if not (CANDIDATE / relative).is_file())
    identical = sorted(
        relative
        for relative, digest in expected.items()
        if (CANDIDATE / relative).is_file() and sha256(CANDIDATE / relative) == digest
    )
    updated = sorted(set(expected) - set(missing) - set(identical))
    if missing:
        raise RuntimeError(f"Judged paths missing from candidate: {missing}")
    if set(updated) != ALLOWED_UPDATED_ENTRYPOINTS:
        raise RuntimeError(f"Unexpected judged-path changes: {updated}")
    if not PROTECTED_PAGES.issubset(identical):
        raise RuntimeError("Historical evidence pages changed")

    candidate_files = [
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    ]
    report = {
        "judged_revision": "0a5097dafd70804544be18562cbdafe265bf4617",
        "old_file_count": len(expected),
        "candidate_file_count": len(candidate_files),
        "old_file_set_is_subset": True,
        "missing_old_paths": [],
        "byte_identical_old_paths": identical,
        "updated_canonical_entrypoints": updated,
        "protected_historical_pages_byte_identical": True,
        "note": (
            "README.md, logbook.json, and pages/index.md are updated only to "
            "make current evidence canonical. Exact historical evidence pages "
            "remain at their original paths and hashes."
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"PROTECTED_SUBSET_OK old={len(expected)} candidate={len(candidate_files)} "
        f"identical={len(identical)} updated={len(updated)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
