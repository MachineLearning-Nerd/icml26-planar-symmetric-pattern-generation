#!/usr/bin/env python3
"""Verify the published documentation, evidence, and provenance contract."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_STATUS = "PARTIAL_C1_C5_VERIFIED_C6_BLOCKED_MECHANICS_B9_ZERO_SHOT_MECHANISM_VERIFIED_HISTORICAL_SCORE_8_OF_12_NO_CURRENT_SCORE"
EXPECTED_BRANCHES = {
    "audit/c2-universal-approximation",
    "audit/c5-vtm-128",
    "audit/c5-vtm-192",
    "audit/c6-mechanics-b9",
    "audit/c6-zero-shot-scope",
    "audit/provider-cpu-metadata",
    "historical/c6-first-12-control",
    "historical/judged-baseline",
    "main",
    "release/canonical-upload-fix",
    "release/evaluator-candidate",
}
EXPECTED_COMMITS = 27
CANONICAL_IDENTITY = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"


def load(path: str):
    return json.loads((ROOT / path).read_text())


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"verification failed: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def published_branches() -> set[str]:
    remote = {
        name.removeprefix("origin/")
        for name in git(
            "for-each-ref", "refs/remotes/origin", "--format=%(refname:short)"
        ).splitlines()
        if name.startswith("origin/") and name != "origin/HEAD"
    }
    return remote or set(git("for-each-ref", "refs/heads", "--format=%(refname:short)").splitlines())


def main() -> None:
    claims = load("claims.json")
    verdicts = load("reproduction_verdicts.json")
    manifest = load("EVIDENCE_MANIFEST.json")
    state = load("AUTONOMOUS_STATE.json")
    source = load(".openresearch/source/source_pin.json")
    c1 = load(".openresearch/artifacts/claims/claim_1/raw_results.json")
    c2 = load(".openresearch/artifacts/claims/claim_2/raw_results.json")
    c3 = load(".openresearch/artifacts/claims/claim_3/raw_results.json")
    c4 = load(".openresearch/artifacts/claims/claim_4/raw_results.json")
    c5 = load(".openresearch/artifacts/claims/claim_5/raw_results.json")
    c6 = load(".openresearch/artifacts/claims/claim_6/raw_results.json")
    review = load("space_candidate/evidence/evaluator_blind_review.json")
    subset = load("space_candidate/evidence/protected_subset_report.json")
    visibility = load("space_candidate/evidence/visibility_matrix.json")
    readme = (ROOT / "README.md").read_text()
    citation = (ROOT / "CITATION.cff").read_text()

    expected_statuses = {
        "C1": "VERIFIED_SCOPED_HIGH",
        "C2": "VERIFIED_SCOPED_MEDIUM",
        "C3": "VERIFIED_SCOPED_HIGH",
        "C4": "VERIFIED_SCOPED_HIGH",
        "C5": "VERIFIED_SCOPED_HIGH",
        "C6": "BLOCKED_PAPER_SCALE",
    }
    require(claims["overall_status"] == EXPECTED_STATUS, "claims overall status")
    require(state["overall_status"] == EXPECTED_STATUS, "state overall status")
    require(verdicts["overall_status"] == EXPECTED_STATUS, "verdict overall status")
    require(verdicts["claim_statuses"] == expected_statuses, "verdict statuses")
    require({claim["id"]: claim["status"] for claim in claims["claims"]} == expected_statuses, "claim statuses")
    require(all((ROOT / path).exists() for path in manifest["required_paths"]), "manifest paths")
    for artifact in manifest["artifacts"]:
        require(sha256(ROOT / artifact["path"]) == artifact["sha256"], f"artifact digest {artifact['path']}")
    require(source["arxiv_id"] == "2606.02073v1", "source revision")
    require(source["sha256"] == manifest["source"]["sha256"], "source digest")
    require("https://arxiv.org/abs/2606.02073" in citation, "citation source")
    require(EXPECTED_STATUS in readme and "Claim 6" in readme and "1,000" in readme, "README status and scope")

    require(c1["status"] == "VERIFIED" and c1["groups_checked"] == 17, "claim 1 result")
    require(c2["status"] == "VERIFIED" and c2["all_proof_obligations_pass"], "claim 2 result")
    require(c3["status"] == "VERIFIED" and c3["groups_checked"] == 17 and c3["max_invariance_error"] < 1e-12, "claim 3 result")
    require(c4["status"] == "VERIFIED" and c4["groups_checked"] == 17 and c4["max_symmetry_error"] < 1e-12, "claim 4 result")
    require(c5["status"] == "VERIFIED" and c5["paper_128_p4mm"]["island_to_connected_ratio"] > 400, "claim 5 result")
    require(c6["status"] == "BLOCKED", "claim 6 blocked result")
    require(c6["homogenization"]["status"] == "VERIFIED", "claim 6 mechanics")
    require(c6["theorem_b9"]["status"] == "VERIFIED", "claim 6 theorem")
    require(c6["zero_shot"]["mechanism_status"] == "VERIFIED", "claim 6 mechanism")
    require(c6["zero_shot"]["samples_per_group"] == 1 and c6["zero_shot"]["paper_samples_per_group"] == 1000, "claim 6 population scope")
    require(c6["zero_shot"]["maximum_direct_residual"] < 1e-8, "claim 6 residual")

    historical = verdicts["historical_external_results"]
    require(historical["baseline"]["score"] == "8/12", "historical score")
    require(historical["baseline"]["current_score_claim"] is False, "historical current score claim")
    require(historical["forecast"]["is_judge_result"] is False, "forecast classification")
    require(verdicts["publication"]["publication_allowed"] is False, "publication state")
    require(verdicts["publication"]["author_endorsement_claimed"] is False, "author endorsement state")
    require(review["latest_pass_complete"] is True and review["passes"][-1]["complete"] is True, "blind review")
    require(subset["old_file_set_is_subset"] is True and subset["missing_old_paths"] == [], "protected subset")
    require(subset["protected_historical_pages_byte_identical"] is True, "protected historical pages")
    require(len(visibility["claims"]) == 6 and all(all(row[field] for field in visibility["required_boolean_fields"]) for row in visibility["claims"]), "visibility matrix")

    branches = published_branches()
    require(branches == EXPECTED_BRANCHES, "published branches")
    require(not any(branch.startswith("orx/") for branch in branches), "legacy orx branch")
    require(int(git("rev-list", "--all", "--count")) == EXPECTED_COMMITS, "reachable commit count")
    identities = git("log", "--all", "--format=%an <%ae>\n%cn <%ce>").splitlines()
    require(identities and all(identity == CANONICAL_IDENTITY for identity in identities), "canonical commit identity")

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(branches)} commits={EXPECTED_COMMITS} "
        "claims=C1:C5_scoped_verified,C6_blocked_paper_scale historical_score=8/12 "
        "current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()
