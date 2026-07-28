# Claim 3 — invariant decomposition

**Verdict: VERIFIED · confidence HIGH**

**Exact claim.** Equation 3 combines affine-reflection-invariant coefficient
functions \(h_i\) with fixed \(G\)-invariant bases \(\eta_i\), so
\(f(x)=\sum_i h_i(x)\eta_i(x)\) is \(G\)-invariant. Source anchor `#S3.E3`;
paper HTML SHA-256 `0d9de93e…d55`.

| Evidence | Result |
| --- | --- |
| Groups | 17/17 |
| Maximum invariance residual | `5.342948306008566e-16` |
| Acceptance threshold | `1e-12` |
| Non-invariant coefficient control | error `2.2096353144938563` |

The finite ledger covers every paper-listed planar group. The logical subgroup
implication is elementary; the floating-point result is a regression check.
Assumptions audited: every coefficient is invariant under the containing
reflection group, every basis is \(G\)-invariant, and the sum is finite.
Limitation: machine-precision tests detect implementation regressions but do
not replace the elementary symbolic implication.

Full regeneration: `uv run --frozen python reproduce.py`. Fast checker:
`uv run --frozen python verify_release.py`.

Evidence: [contract](../../evidence/claims/claim_3/claim_contract.json) ·
[source audit](../../evidence/claims/claim_3/source_audit.md) ·
[method](../../evidence/claims/claim_3/method.md) ·
[raw JSON](../../evidence/claims/claim_3/raw_results.json) ·
[checker](../../evidence/claims/claim_3/checker_output.json) ·
[control](../../evidence/claims/claim_3/negative_control_output.json) ·
[environment](../../evidence/claims/claim_3/run_environment.json) ·
[code](../../repro/baseline.py)

Run `be3f0b80-0cad-420e-a04b-fbe56ce5c7e5`, Git `ccf8fe2`, deterministic
seed ledger, Python 3.12.12 in the locked `uv` environment. Estimated 1 core;
cumulative provider allocation 8 vCPUs on HF `cpu-upgrade`, with 64 logical
CPUs visible; the claim-local check finishes in under one scientific second.
