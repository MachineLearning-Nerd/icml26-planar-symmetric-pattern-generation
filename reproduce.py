#!/usr/bin/env python3
"""Fixed campaign entrypoint.

Experiment branches change campaign_config.json and add claim modules.  The
OpenResearch run command stays ``uv run --frozen python reproduce.py``.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from pathlib import Path

from repro.baseline import run_baseline
from repro.claim2_proof import verify_claim_2
from repro.claim5_vtm import verify_claim_5


ROOT = Path(__file__).resolve().parent


def cpu_allocation() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def main() -> int:
    started = time.perf_counter()
    config = json.loads((ROOT / "campaign_config.json").read_text())
    report = {
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "estimated_scientific_cores": config["estimated_scientific_cores"],
            "selected_backend": config["selected_backend"],
            "selected_flavor": config["selected_flavor"],
            "actual_cpu_allocation": cpu_allocation(),
            "seed": config["seed"],
        },
        "stage": config["stage"],
        "claims": {},
    }
    baseline = run_baseline(config["seed"])
    report["claims"].update(baseline["claims"])
    report["negative_controls"] = baseline["negative_controls"]
    if config["stage"] != "judged_baseline":
        claim_2, claim_2_controls = verify_claim_2()
        report["claims"]["claim_2"] = claim_2
        report["negative_controls"]["claim_2_proof_certificate"] = claim_2_controls
    if config["stage"].startswith("claim5_vtm"):
        claim_5, claim_5_controls = verify_claim_5(config)
        report["claims"]["claim_5"] = claim_5
        report["negative_controls"]["claim_5_vtm"] = claim_5_controls
    report["runtime_seconds"] = time.perf_counter() - started
    report["release_gate"] = {
        "previously_full_credit_regression_pass": all(
            report["claims"][key]["status"] == "VERIFIED"
            for key in ("claim_1", "claim_3", "claim_4")
        ),
        "baseline_judged_score": "8/12",
        "score_change_claimed": False,
    }
    output = ROOT / ".openresearch" / "artifacts" / "baseline" / "raw_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("=== OPENRESEARCH_EVIDENCE_JSON_BEGIN ===")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("=== OPENRESEARCH_EVIDENCE_JSON_END ===")
    current_claims_pass = all(
        report["claims"][key]["status"] == "VERIFIED"
        for key in ("claim_1", "claim_2", "claim_3", "claim_4", "claim_5")
    )
    report["release_gate"]["current_claims_pass"] = current_claims_pass
    ok = (
        report["release_gate"]["previously_full_credit_regression_pass"]
        and current_claims_pass
    )
    if not ok:
        print("REGRESSION FAILURE: a previously full-credit claim did not pass", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
