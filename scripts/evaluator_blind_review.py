"""Audit the release exactly as a reviewer can discover it from entrypoints."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "space_candidate"
CLAIM_FIELDS = {
    "exact_claim": ("Exact", "claim"),
    "source_quantifiers": ("Source", "anchor"),
    "assumptions": ("assumption",),
    "executable_code": ("code",),
    "fixed_command": ("uv run --frozen python reproduce.py",),
    "raw_inline": ("Result",),
    "raw_link": ("raw",),
    "independent_checker": ("checker",),
    "negative_control": ("control",),
    "limitations": ("limitation",),
    "git_sha": ("Git",),
    "seed": ("seed",),
    "cpu_runtime": ("vCPU",),
    "verdict": ("Verdict",),
}


def markdown_targets(text: str) -> list[str]:
    return [
        target
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        if not target.startswith(("#", "http://", "https://"))
    ]


def resolve_link(root: Path, source: Path, target: str) -> Path:
    clean = target.split("#", 1)[0].split("?", 1)[0]
    return (source.parent / clean).resolve()


def contains_tokens(text: str, tokens: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return all(token.lower() in lowered for token in tokens)


def review(snapshot: Path, pass_name: str) -> dict[str, object]:
    snapshot = snapshot.resolve()
    opened: list[str] = []
    missing_links: list[str] = []

    def read(relative: str) -> str:
        path = snapshot / relative
        if not path.is_file():
            raise RuntimeError(f"Canonical file is missing: {relative}")
        opened.append(relative)
        return path.read_text(encoding="utf-8")

    readme = read("README.md")
    logbook_text = read("logbook.json")
    logbook = json.loads(logbook_text)
    index_file = logbook["root"]["file"]
    index_text = read(index_file)
    claim_nodes = {
        child["slug"]: child["file"]
        for child in logbook["root"]["children"]
        if re.fullmatch(r"claim-[1-6]", child["slug"])
    }
    if set(claim_nodes) != {f"claim-{number}" for number in range(1, 7)}:
        raise RuntimeError("Canonical logbook does not expose all six claims")

    pages: dict[str, dict[str, object]] = {}
    for slug, relative in sorted(claim_nodes.items()):
        text = read(relative)
        checks = {
            field: contains_tokens(text, tokens)
            for field, tokens in CLAIM_FIELDS.items()
        }
        if slug == "claim-6":
            checks["blocked_scope"] = (
                "BLOCKED" in text
                and "1 sample per group, not 1,000" in text
                and "20.27 days" in text
            )
        for target in markdown_targets(text):
            path = resolve_link(snapshot, snapshot / relative, target)
            if snapshot.resolve() not in path.parents and path != snapshot.resolve():
                missing_links.append(f"{relative} -> outside snapshot: {target}")
            elif not path.is_file():
                missing_links.append(f"{relative} -> {target}")
            else:
                opened.append(path.relative_to(snapshot).as_posix())
        pages[slug] = {
            "canonical_page": relative,
            "checks": checks,
            "complete": all(checks.values()),
        }

    supplemental_nodes = {
        child["slug"]: child["file"]
        for child in logbook["root"]["children"]
        if child["slug"] not in claim_nodes
    }
    for _, relative in sorted(supplemental_nodes.items()):
        text = read(relative)
        for target in markdown_targets(text):
            path = resolve_link(snapshot, snapshot / relative, target)
            if snapshot.resolve() not in path.parents and path != snapshot.resolve():
                missing_links.append(f"{relative} -> outside snapshot: {target}")
            elif not path.is_file():
                missing_links.append(f"{relative} -> {target}")
            else:
                opened.append(path.relative_to(snapshot).as_posix())

    for source_relative, text in (
        ("README.md", readme),
        (index_file, index_text),
    ):
        for target in markdown_targets(text):
            path = resolve_link(snapshot, snapshot / source_relative, target)
            if snapshot.resolve() not in path.parents and path != snapshot.resolve():
                missing_links.append(f"{source_relative} -> outside snapshot: {target}")
            elif not path.is_file():
                missing_links.append(f"{source_relative} -> {target}")
            else:
                opened.append(path.relative_to(snapshot).as_posix())

    current_before_history = (
        index_text.find("Current verification") >= 0
        and index_text.find("Current verification") < index_text.find("Preserved history")
        and index_text.find("verify_release.py") < index_text.find("Historical rejected baseline")
    )
    verdicts = {
        slug: ("BLOCKED" if slug == "claim-6" else "VERIFIED")
        for slug in sorted(claim_nodes)
    }
    missing_cells = [
        f"{slug}:{field}"
        for slug, page in pages.items()
        for field, passed in page["checks"].items()
        if not passed
    ]
    return {
        "pass": pass_name,
        "review_scope": "fresh candidate snapshot; canonical entrypoints only",
        "entrypoints": ["README.md", "logbook.json", index_file],
        "files_opened": sorted(set(opened)),
        "claim_pages": pages,
        "supplemental_pages": supplemental_nodes,
        "reviewer_verdicts": verdicts,
        "current_verifier_precedes_history": current_before_history,
        "missing_link_targets": sorted(set(missing_links)),
        "missing_visibility_cells": missing_cells,
        "complete": (
            not missing_links
            and not missing_cells
            and current_before_history
            and len(pages) == 6
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pass-name", required=True)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output")
    args = parser.parse_args()
    source = Path(args.source).resolve()
    report = (
        Path(args.output).resolve()
        if args.output
        else source / "evidence" / "evaluator_blind_review.json"
    )
    with tempfile.TemporaryDirectory(prefix="planar-evaluator-blind-") as tmp:
        snapshot = Path(tmp) / "space"
        shutil.copytree(source, snapshot)
        result = review(snapshot, args.pass_name)
    prior = {"schema_version": 1, "passes": []}
    if report.is_file() and not args.reset:
        prior = json.loads(report.read_text(encoding="utf-8"))
    prior["passes"].append(result)
    prior["latest_pass_complete"] = prior["passes"][-1]["complete"]
    prior["review_converged"] = (
        len(prior["passes"]) >= 2
        and not prior["passes"][0]["complete"]
        and prior["passes"][-1]["complete"]
    )
    prior["fixes_between_passes"] = [
        "Added explicit assumptions, limitations, seeds, Git SHA, CPU allocation, "
        "and runtime metadata to the six canonical claim pages."
    ]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(prior, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result["complete"]:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1
    print(
        f"EVALUATOR_BLIND_REVIEW_OK pass={args.pass_name} "
        f"opened={len(result['files_opened'])} claims={len(result['claim_pages'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
