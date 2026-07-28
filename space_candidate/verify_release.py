"""Fast, independent checker for the committed evaluator-visible evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INTERNAL = ROOT / ".openresearch" / "artifacts" / "claims"
PUBLIC = ROOT / "evidence" / "claims"
CLAIMS = INTERNAL if INTERNAL.exists() else PUBLIC


def load(claim: int, name: str) -> dict:
    return json.loads((CLAIMS / f"claim_{claim}" / name).read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    c1 = load(1, "raw_results.json")
    require(c1["status"] == "VERIFIED", "Claim 1 verdict")
    require(c1["groups_checked"] == 17, "Claim 1 complete group ledger")
    require(load(1, "checker_output.json")["all_checks_pass"], "Claim 1 checks")
    require(load(1, "negative_control_output.json")["passes"], "Claim 1 control")

    c2 = load(2, "raw_results.json")
    require(c2["status"] == "VERIFIED", "Claim 2 verdict")
    require(c2["all_proof_obligations_pass"], "Claim 2 proof obligations")
    require(c2["strict_budget_instance"]["strictly_below_epsilon"], "Claim 2 L1 budget")
    require(load(2, "checker_output.json")["all_checks_pass"], "Claim 2 checks")
    require(
        load(2, "negative_control_output.json")["all_negative_controls_pass"],
        "Claim 2 controls",
    )

    for claim, metric in ((3, "max_invariance_error"), (4, "max_symmetry_error")):
        raw = load(claim, "raw_results.json")
        require(raw["status"] == "VERIFIED", f"Claim {claim} verdict")
        require(raw["groups_checked"] == 17, f"Claim {claim} complete group ledger")
        require(raw[metric] < 1e-12, f"Claim {claim} numerical threshold")
        require(
            load(claim, "negative_control_output.json")["passes"],
            f"Claim {claim} control",
        )

    c5 = load(5, "raw_results.json")
    require(c5["status"] == "VERIFIED", "Claim 5 verdict")
    require(
        c5["paper_128_p4mm"]["island_to_connected_ratio"] > 400,
        "Claim 5 VTM separation",
    )
    require(
        c5["paper_128_p4mm"]["connected_unreachable_material_cells"] == 0
        and c5["paper_128_p4mm"]["island_unreachable_material_cells"] > 0,
        "Claim 5 independent connectivity oracle",
    )
    require(load(5, "checker_output.json")["all_checks_pass"], "Claim 5 checks")
    require(
        load(5, "negative_control_output.json")["all_negative_controls_pass"],
        "Claim 5 controls",
    )

    c6 = load(6, "raw_results.json")
    require(c6["status"] == "BLOCKED", "Claim 6 must remain honestly BLOCKED")
    require(c6["homogenization"]["status"] == "VERIFIED", "Claim 6 mechanics")
    require(c6["theorem_b9"]["status"] == "VERIFIED", "Claim 6 theorem")
    require(
        c6["theorem_b9"]["certificate_sha256"]
        == sha256(CLAIMS / "claim_6" / "theorem_b9_certificate.json"),
        "Claim 6 theorem certificate hash",
    )
    require(
        c6["zero_shot"]["mechanism_status"] == "VERIFIED"
        and c6["zero_shot"]["status"] == "BLOCKED",
        "Claim 6 scoped/full distinction",
    )
    require(
        c6["zero_shot"]["samples_per_group"] == 1
        and c6["zero_shot"]["paper_samples_per_group"] == 1000,
        "Claim 6 population scope",
    )
    require(
        c6["zero_shot"]["maximum_direct_residual"] < 1e-8,
        "Claim 6 independent equilibrium",
    )
    require(
        c6["zero_shot"]["provider_allocated_vcpus"] == 8
        and c6["zero_shot"]["container_visible_logical_cpus"] == 64,
        "Claim 6 allocated/visible CPU distinction",
    )
    require(
        c6["zero_shot"]["observed_concurrent_primary_workers"] == 12
        and c6["zero_shot"]["paper_scale_ideal_worker_waves"] == 1000
        and c6["zero_shot"]["paper_scale_checked_lower_bound_days"] > 6,
        "Claim 6 non-circular paper-scale calibration",
    )
    require(len(load(6, "zero_shot_rows.json")) == 12, "Claim 6 row ledger")
    require(
        load(6, "negative_control_output.json")["all_required_controls_pass"],
        "Claim 6 controls",
    )

    candidate = ROOT if (ROOT / "pages").exists() else ROOT / "space_candidate"
    historical = {
        "pages/verify/page.md": "14719a2b9196de145ccd38dd87d9816650e86d7dd838d4518c9ce5b17ccd3711",
        "pages/overview/page.md": "ff176a2f3799b79665bc1530c405412ae6dbe0849bb917c0a6b258b395f21a0d",
    }
    if candidate.exists():
        for relative, expected in historical.items():
            require(sha256(candidate / relative) == expected, f"protected {relative}")
        matrix = json.loads((candidate / "evidence" / "visibility_matrix.json").read_text())
        require(len(matrix["claims"]) == 6, "visibility matrix row count")
        require(
            all(all(row[field] for field in matrix["required_boolean_fields"]) for row in matrix["claims"]),
            "visibility matrix has a missing cell",
        )

    print("RELEASE_EVIDENCE_VERIFIED: claims 1-5 VERIFIED; claim 6 BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
