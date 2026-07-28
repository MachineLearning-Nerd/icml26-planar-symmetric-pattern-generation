# Claim 2 — universal approximation

**Verdict: VERIFIED · confidence MEDIUM**

**Exact claim.** For every continuous \(G\)-invariant function and every
\(\epsilon>0\), Theorem 3.3 asserts the existence of coefficient functions
\(h_1,\ldots,h_r\) in the Equation 3 decomposition whose \(L^1(\Omega)\)
approximation error is below \(\epsilon\). Source anchors: Theorem 3.3 and
Appendix C.4; paper HTML SHA-256 `0d9de93e…d55`.

This supersedes the historical one-target p4mm curve. The current certificate
reconstructs the universal argument, rather than extrapolating a finite sweep:

Assumptions audited: compact domain, continuous finite-group action,
continuous \(G\)-invariant target, every \(\epsilon>0\), the \(L^1\) error
norm, Reynolds averaging, and the finite Hironaka module decomposition.

| Proof obligation | Result |
| --- | --- |
| Quantifier order and L1 norm | exact |
| Compact-domain density | checked |
| Reynolds averaging contraction | operator norm ≤ 1 |
| Hironaka module decomposition | algebraic residual 0 |
| Strict error budget | `0.0625 < epsilon=0.125` |
| Planar rank ledger | complete |
| Non-circularity | no fitted sample count or target |

Certificate SHA-256:
`8e97fe2cb456bfd1365827699bd64bf694c4dec08c0b888eb8a90759904776e2`.
Deleting the Hironaka step, changing a catalogue rank, or using an excessive
uniform tolerance each makes the checker fail.

Limitation: this is an independently reconstructed symbolic certificate, not
a Lean/Coq kernel proof. That is the material remaining validation risk behind
MEDIUM confidence.

Full regeneration: `uv run --frozen python reproduce.py`. Fast checker:
`uv run --frozen python verify_release.py`.

Evidence: [contract](../../evidence/claims/claim_2/claim_contract.json) ·
[source audit](../../evidence/claims/claim_2/source_audit.md) ·
[method](../../evidence/claims/claim_2/method.md) ·
[certificate](../../evidence/claims/claim_2/proof_certificate.json) ·
[raw JSON](../../evidence/claims/claim_2/raw_results.json) ·
[checker](../../evidence/claims/claim_2/checker_output.json) ·
[controls](../../evidence/claims/claim_2/negative_control_output.json) ·
[environment](../../evidence/claims/claim_2/run_environment.json) ·
[code](../../repro/claim2_proof.py)

Dedicated run `f79c9162-8380-4bf8-9db9-b46e09c6bd57`; cumulative run
`be3f0b80-0cad-420e-a04b-fbe56ce5c7e5`; deterministic certificate; scientific
runtime 0.333 s. Git `ccf8fe2598f08cf010ed20ea63e266a36b5641b4`;
seed: no RNG is used. Estimated 1 core; actual cumulative allocation 64 vCPUs
on HF `cpu-upgrade`.
