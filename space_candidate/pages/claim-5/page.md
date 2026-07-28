# Claim 5 — VTM connectivity

**Verdict: VERIFIED · confidence HIGH**

**Exact claim.** Equation 6's Virtual Temperature Method loss penalizes
globally disconnected material while the symmetric representation preserves
the required planar symmetry. Source anchors: Section 6.2, Equation 6,
Figure 4, Appendix E.3/F.2; paper HTML SHA-256 `0d9de93e…d55`.

The current verifier uses the exact released VTM finite-element source at
commit `b6a27ef…`, the paper's 128×128 Q1 mesh, a 2×2 periodic p4mm
supercell, \(q_0=10^{-4}\), conductivity \([10^{-4},1]\), SIMP 5, and p=20.
Assumptions audited: positive conductivity, the released Q1 discretization,
periodic boundary identification, connected boundary sources, p=20
aggregation, and exactly symmetric connected/disconnected density fields.

| 128×128 evidence | Connected | Periodic islands |
| --- | ---: | ---: |
| Unreachable material cells | 0 | 1,936 |
| VTM p20 score | 1.9474 | 781.3051 |
| Linear residual | `3.71e-7` | `4.54e-7` |
| Symmetry/translation error | 0 | 0 |

The island score is **401.2×** the connected score. An independent flood fill
produces the reachability counts, independent score recomputation differs by
zero, and a fixed 0.01 released-adjoint step reduces the island score by
12.04%. A second released 192×192 p6mm route gives 641.2× separation. Single
pixel symmetry and periodicity breaks are rejected as intended.

Limitations: this verifies the VTM connectivity mechanism and adjoint, not
SDXL image generation or physical paper fabrication. It does not assert that
every optimizer trajectory reaches connectivity.

Full regeneration: `uv run --frozen python reproduce.py`. Fast checker:
`uv run --frozen python verify_release.py`.

Evidence: [contract](../../evidence/claims/claim_5/claim_contract.json) ·
[source audit](../../evidence/claims/claim_5/source_audit.md) ·
[method](../../evidence/claims/claim_5/method.md) ·
[raw JSON](../../evidence/claims/claim_5/raw_results.json) ·
[checker](../../evidence/claims/claim_5/checker_output.json) ·
[controls](../../evidence/claims/claim_5/negative_control_output.json) ·
[environment](../../evidence/claims/claim_5/run_environment.json) ·
[code](../../repro/claim5_vtm.py)

Paper run `18f6dd71-7dc6-4254-ae74-a986b2aaacf5`: estimate 8 cores,
provider allocation 8 vCPUs (64 logical visible), 41.07 scientific seconds.
Released-configuration run
`ebeeffbd-20ea-4abe-89f7-08465ee2a608`: 50.24 scientific seconds. Git
`ccf8fe2598f08cf010ed20ea63e266a36b5641b4`; seed: deterministic analytic
density fields, no RNG.
