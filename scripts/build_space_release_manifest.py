"""Build and verify the exact text-only Hugging Face Space upload set."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPACE = ROOT / "space_candidate"
ALLOWLIST = SPACE / "evidence" / "upload_allowlist.txt"
MANIFEST = SPACE / "evidence" / "upload_manifest.sha256"
EXACT_FILES = {
    ".python-version",
    "README.md",
    "campaign_config.json",
    "logbook.json",
    "pages/index.md",
    "pyproject.toml",
    "reproduce.py",
    "uv.lock",
    "verify_release.py",
}
PREFIXES = (
    "evidence/",
    "notebooks/",
    "pages/claim-",
    "pages/release/",
    "reports/",
    "repro/",
)
EXCLUDED = {
    "evidence/upload_allowlist.txt",
    "evidence/upload_manifest.sha256",
}
TEXT_SUFFIXES = {".json", ".lock", ".md", ".py", ".svg", ".toml", ".txt"}


def selected(relative: str) -> bool:
    path = Path(relative)
    return (
        relative in EXACT_FILES
        or any(relative.startswith(prefix) for prefix in PREFIXES)
    ) and (path.suffix in TEXT_SUFFIXES or relative == ".python-version")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    payload = []
    for path in sorted(SPACE.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(SPACE).as_posix()
        if selected(relative) and relative not in EXCLUDED:
            path.read_text(encoding="utf-8")
            payload.append(relative)

    upload_paths = payload + sorted(EXCLUDED)
    ALLOWLIST.write_text("\n".join(upload_paths) + "\n", encoding="utf-8")
    manifest_paths = payload + ["evidence/upload_allowlist.txt"]
    MANIFEST.write_text(
        "".join(
            f"{digest(SPACE / relative)}  {relative}\n"
            for relative in manifest_paths
        ),
        encoding="utf-8",
    )

    require = set(upload_paths)
    observed = set(ALLOWLIST.read_text(encoding="utf-8").splitlines())
    if require != observed:
        raise RuntimeError("Upload allowlist did not round-trip")
    if "pages/verify/page.md" in require or "pages/overview/page.md" in require:
        raise RuntimeError("Protected historical pages must not be re-uploaded")
    print(
        f"TEXT_UPLOAD_ALLOWLIST_OK files={len(upload_paths)} "
        f"hashed={len(manifest_paths)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
