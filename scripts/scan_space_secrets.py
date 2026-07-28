"""Fail when the exact text upload set contains credential-like material."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPACE = ROOT / "space_candidate"
ALLOWLIST = SPACE / "evidence" / "upload_allowlist.txt"
REPORT = SPACE / "evidence" / "secret_scan.json"
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "hugging_face_token": re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "bearer_token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b"),
    "assigned_secret": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b"
        r"\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']"
    ),
}


def main() -> int:
    paths = ALLOWLIST.read_text(encoding="utf-8").splitlines()
    findings: list[dict[str, object]] = []
    for relative in paths:
        text = (SPACE / relative).read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for name, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(
                        {
                            "path": relative,
                            "line": line_number,
                            "pattern": name,
                        }
                    )
    result = {
        "scope": "exact text-only upload allowlist",
        "files_scanned": len(paths),
        "patterns": sorted(PATTERNS),
        "findings": findings,
        "passed": not findings,
        "note": "No credential values are printed or stored in this report.",
    }
    REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if findings:
        print(f"SECRET_SCAN_FAILED findings={len(findings)}")
        return 1
    print(f"SECRET_SCAN_OK files={len(paths)} findings=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
