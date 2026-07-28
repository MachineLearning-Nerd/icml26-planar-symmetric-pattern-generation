# Claim 1 — conjugation into reflection groups

**Verdict: VERIFIED · confidence HIGH**

**Exact claim.** Theorem 3.2 states that for any planar symmetry group \(G\),
there is an invertible linear transformation conjugating \(G\) to a subgroup
of an affine reflection group. Source anchor: Theorem 3.2 (`#S3.Thmtheorem2`);
paper HTML SHA-256 `0d9de93e…d55`.

The complete finite planar catalogue was checked:

| Evidence | Result |
| --- | --- |
| Point-group representatives | 17/17 |
| Subgroup checks | 17/17 |
| Distort then inverse-conjugate recovery | 17/17 |
| Intended-failure control | `p6 < D4` correctly rejected |

Assumption audit and scope: the ledger exhausts the 17 planar point-group
representatives used by the paper. It is finite regression evidence and does
not replace the abstract theorem proof for arbitrary affine realizations.
Limitation: this is exhaustive over the stated finite catalogue but is not a
proof-kernel certificate for the abstract theorem. Seed: no stochastic
sampling is used; the catalogue and matrices are deterministic.

Full regeneration: `uv run --frozen python reproduce.py`. Fast evidence
checker: `uv run --frozen python verify_release.py`. Both exit nonzero on a
failed required check.

Evidence: [contract](../../evidence/claims/claim_1/claim_contract.json) ·
[source audit](../../evidence/claims/claim_1/source_audit.md) ·
[method](../../evidence/claims/claim_1/method.md) ·
[raw JSON](../../evidence/claims/claim_1/raw_results.json) ·
[checker](../../evidence/claims/claim_1/checker_output.json) ·
[control](../../evidence/claims/claim_1/negative_control_output.json) ·
[environment](../../evidence/claims/claim_1/run_environment.json) ·
[code](../../repro/baseline.py)

Evidence run `be3f0b80-0cad-420e-a04b-fbe56ce5c7e5`, Git
`ccf8fe2598f08cf010ed20ea63e266a36b5641b4`, Python 3.12.12, locked `uv`
environment. Claim-local estimate 1 core; it ran within the 64-vCPU cumulative
HF `cpu-upgrade` job.
