# Claim 4 — all-group pattern generation

**Verdict: VERIFIED · confidence HIGH**

**Exact claim.** Algorithm 1 maps query points into the asymmetric unit and
combines coefficients with fixed bases to generate patterns respecting all 17
planar groups. Source anchors: Algorithm 1 (`#S3.A1`) and Section 6.1; paper
HTML SHA-256 `0d9de93e…d55`.

| Evidence | Result |
| --- | --- |
| Groups | 17/17 |
| Maximum symmetry residual | `1.6237011735142914e-15` |
| Acceptance threshold | `1e-12` |
| No-projection control | error `2.4099611004140677` |

This verifies the symmetry guarantee, not text-image aesthetics or human
preference.
Assumptions audited: the paper-listed first 17 planar groups, deterministic
query points, asymmetric-unit projection, and fixed invariant bases.
Limitation: this checks the exact symmetry contract, not prompt adherence or
the perceptual quality of generated images.

Full regeneration: `uv run --frozen python reproduce.py`. Fast checker:
`uv run --frozen python verify_release.py`.

Evidence: [contract](../../evidence/claims/claim_4/claim_contract.json) ·
[source audit](../../evidence/claims/claim_4/source_audit.md) ·
[method](../../evidence/claims/claim_4/method.md) ·
[raw JSON](../../evidence/claims/claim_4/raw_results.json) ·
[checker](../../evidence/claims/claim_4/checker_output.json) ·
[control](../../evidence/claims/claim_4/negative_control_output.json) ·
[environment](../../evidence/claims/claim_4/run_environment.json) ·
[code](../../repro/baseline.py)

Run `be3f0b80-0cad-420e-a04b-fbe56ce5c7e5`, Git `ccf8fe2`, deterministic
seed ledger, Python 3.12.12 in the locked `uv` environment. Estimated 1 core;
cumulative provider allocation 8 vCPUs on HF `cpu-upgrade`, with 64 logical
CPUs visible; the claim-local check finishes in under one scientific second.
