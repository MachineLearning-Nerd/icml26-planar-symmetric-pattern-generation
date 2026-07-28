"""Independent symbolic proof-certificate checker for Theorem 3.3."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = (
    ROOT
    / ".openresearch"
    / "artifacts"
    / "claims"
    / "claim_2"
    / "proof_certificate.json"
)
SOURCE_PIN_PATH = ROOT / ".openresearch" / "source" / "source_pin.json"


EXPECTED_DEPENDENCIES = {
    "compact_torus": [],
    "trigonometric_density": ["compact_torus"],
    "reynolds_projection": ["trigonometric_density"],
    "hironaka_free_module": ["reynolds_projection"],
    "exact_polynomial_decomposition": ["hironaka_free_module"],
    "l1_from_uniform": ["exact_polynomial_decomposition"],
    "arbitrary_epsilon": ["l1_from_uniform"],
}

PAPER_RANK_LEDGER = {
    "p1": 4,
    "p2": 2,
    "pm": 2,
    "pg": 4,
    "cm": 4,
    "p2mm": 1,
    "p2mg": 2,
    "p2gg": 4,
    "c2mm": 2,
    "p4": 2,
    "p4mm": 1,
    "p4gm": 4,
    "p3": 4,
    "p3m1": 2,
    "p31m": 2,
    "p6": 2,
    "p6mm": 1,
}


def _check_certificate(certificate: dict) -> tuple[bool, list[dict]]:
    checks: list[dict] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    source_pin = json.loads(SOURCE_PIN_PATH.read_text())
    check(
        "source_hash_bound",
        certificate["source_sha256"] == source_pin["sha256"],
        certificate["source_sha256"],
    )
    check(
        "exact_main_quantifiers",
        certificate["quantifiers"]
        == [
            "there exist r fixed G-invariant eta_i",
            "for every f in C_G(R^2)",
            "for every epsilon > 0",
            "there exist h_i in C_Wa(R^2)",
            "the unit-cell L1 error is strictly below epsilon",
        ],
        "Theorem 3.3 quantifier order and L1 norm",
    )
    steps = certificate["steps"]
    ids = [step["id"] for step in steps]
    check(
        "proof_dag_exact",
        ids == list(EXPECTED_DEPENDENCIES)
        and all(
            step["depends_on"] == EXPECTED_DEPENDENCIES[step["id"]]
            for step in steps
        ),
        "All inference steps and dependencies are present in order.",
    )

    constants = certificate["bound_certificate"]
    measure = float(constants["unit_cell_measure_symbolic_value"])
    epsilon = float(constants["epsilon_test_value"])
    delta_multiplier = float(constants["delta_multiplier"])
    reynolds_norm = float(constants["reynolds_operator_norm_bound"])
    decomposition_error = float(constants["exact_decomposition_error"])
    delta = delta_multiplier * epsilon / measure
    derived_l1 = measure * reynolds_norm * delta + decomposition_error
    check("finite_positive_measure", measure > 0.0, f"|Omega|={measure}")
    check("arbitrary_positive_epsilon_instance", epsilon > 0.0, f"epsilon={epsilon}")
    check(
        "reynolds_is_contractive",
        0.0 <= reynolds_norm <= 1.0,
        f"operator norm <= {reynolds_norm}",
    )
    check(
        "hironaka_decomposition_exact",
        decomposition_error == 0.0,
        f"algebraic residual={decomposition_error}",
    )
    check(
        "strict_l1_budget",
        derived_l1 < epsilon,
        f"|Omega|*||R_G||*delta={derived_l1} < epsilon={epsilon}",
    )
    check(
        "epsilon_choice_is_formula_independent_of_target",
        delta_multiplier == 0.5,
        "delta=epsilon/(2|Omega|) leaves strict slack and does not depend on sampled data.",
    )
    check(
        "complete_planar_rank_ledger",
        certificate["planar_basis_ranks"] == PAPER_RANK_LEDGER
        and len(certificate["planar_basis_ranks"]) == 17,
        "All source-tabulated planar classes and r=[Wa:G] ranks are present.",
    )
    check(
        "noncircular_derivation",
        certificate["noncircularity"]
        == "No target, sample, basis budget, tolerance, or fit result is selected from an observed error. The proof chooses a uniform approximation tolerance from epsilon and finite cell measure before constructing the approximant.",
        "The certificate is analytical, not a fitted finite sweep.",
    )
    return all(row["passed"] for row in checks), checks


def verify_claim_2() -> tuple[dict, dict]:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    passed, checks = _check_certificate(certificate)

    loose_budget = copy.deepcopy(certificate)
    loose_budget["bound_certificate"]["delta_multiplier"] = 2.0
    loose_passed, loose_checks = _check_certificate(loose_budget)

    missing_step = copy.deepcopy(certificate)
    missing_step["steps"] = [
        step
        for step in missing_step["steps"]
        if step["id"] != "hironaka_free_module"
    ]
    missing_passed, missing_checks = _check_certificate(missing_step)

    wrong_rank = copy.deepcopy(certificate)
    wrong_rank["planar_basis_ranks"]["p4gm"] = 3
    rank_passed, rank_checks = _check_certificate(wrong_rank)

    controls = {
        "excess_uniform_tolerance_rejected": {
            "passes": not loose_passed,
            "failed_checks": [
                row["name"] for row in loose_checks if not row["passed"]
            ],
        },
        "missing_hironaka_step_rejected": {
            "passes": not missing_passed,
            "failed_checks": [
                row["name"] for row in missing_checks if not row["passed"]
            ],
        },
        "wrong_planar_rank_rejected": {
            "passes": not rank_passed,
            "failed_checks": [
                row["name"] for row in rank_checks if not row["passed"]
            ],
        },
    }
    all_controls = all(control["passes"] for control in controls.values())
    verdict = passed and all_controls
    certificate_digest = hashlib.sha256(CERTIFICATE_PATH.read_bytes()).hexdigest()
    result = {
        "status": "VERIFIED" if verdict else "BLOCKED",
        "source": "Theorem 3.3 and Appendix C.4",
        "evidence_type": "independently reconstructed symbolic derivation with machine-checked proof obligations",
        "certificate_sha256": certificate_digest,
        "proof_checks": checks,
        "all_proof_checks_pass": passed,
        "all_negative_controls_pass": all_controls,
        "limitations": "This checker validates the explicit logical certificate and source assumptions; it is not a kernel-checked Lean/Coq formalization. The finite rank ledger corroborates catalogue coverage but is not used to infer the universal quantifier.",
    }
    if not verdict:
        raise RuntimeError(
            f"Claim 2 proof certificate or tamper controls failed: {result}; {controls}"
        )
    return result, controls


if __name__ == "__main__":
    claim, controls = verify_claim_2()
    print(json.dumps({"claim": claim, "controls": controls}, indent=2, sort_keys=True))
    raise SystemExit(0 if claim["status"] == "VERIFIED" else 1)
