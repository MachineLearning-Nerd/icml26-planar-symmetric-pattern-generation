# Claim 6 — mechanics, 3D theorem, and zero-shot metamaterials

**Verdict: BLOCKED · confidence MEDIUM**

**Exact bundled claim.** Equation 8 applies periodic homogenization objectives
under symmetry constraints; Theorem B.9 universally extends the construction
to three-dimensional space groups; Figure 8 evaluates zero-shot metamaterial
generation on the first 12 planar groups with **1,000 samples per setting**.
Source anchors: `#S5.E8`, `#A2.Thmtheorem9`, `#S6.F8`, Section 6.4; paper
HTML SHA-256 `0d9de93e…d55`.

Assumptions audited: periodic positive-stiffness cells and the released
homogenization solver for Equation 8; crystallographic space groups and
rational lattice forms for Theorem B.9; and the pinned p1-only epoch-99 model,
first 12 group settings, 300-step algorithm, seed 42, and 1,000 samples per
setting for Figure 8.

## Verified components

| Component | Direct evidence |
| --- | --- |
| Homogenization analytic check | full solid 2.857142857; meshes 64/128 agree |
| Released adjoint | central FD relative error `4.90e-4` |
| Fixed-volume direction | bulk `0.00072359 → 0.00074659`; opposite `0.00070084` |
| Theorem B.9 certificate | 9/9 obligations and 3/3 tamper controls |

The B.9 certificate covers the two 2D maximal integral classes, three cubic 3D
lattice classes, root/dual B3/C3 coverage, rational SPD averaging, and affine
translation lift. It is independently reconstructed, not Lean/Coq.

## Scoped zero-shot calibration

The pinned epoch-99 p1-only checkpoint has no symmetry label. The exact
300-step AdamW/SDS algorithm at 64×64, seed 42, ran once for each first-12
group, plus an independent p4mm replay.

| Evidence | Result |
| --- | ---: |
| Unique masks | 12/12 |
| Volume MAE | **1.2126%** (paper threshold 1.5%) |
| Maximum binary symmetry mismatch | **0.2225%** |
| Maximum direct equilibrium residual | `3.25e-9` |
| Median generated / void bulk | `7.175e-6 / 2.857e-6` |
| p1 falsely tested as p4mm | 44.16% mismatch |
| p4mm deterministic replay | exact same SHA-256 |

The released native CG path reaches residual `0.380` on one mask. That
limitation is preserved inline; the current checker independently solves the
assembled systems with SciPy direct sparse factorization.

## Why the verdict is BLOCKED

This ran **1 sample per group, not 1,000**. The accepted replay observed all 12
primary workers concurrently, so 12,000 checked samples require at least 1,000
ideal waves. The observed slowest primary worker gives **6.09 days** before
provisioning, failures, or report overhead. HF allocates 8 vCPUs/32 GB while
the container exposes 64 logical CPUs; neither is misreported as the other.
No population-distribution conclusion is made.

Full regeneration: `uv run --frozen python reproduce.py`. Fast checker:
`uv run --frozen python verify_release.py`.

Evidence: [contract](../../evidence/claims/claim_6/claim_contract.json) ·
[source audit](../../evidence/claims/claim_6/source_audit.md) ·
[method](../../evidence/claims/claim_6/method.md) ·
[zero-shot method](../../evidence/claims/claim_6/zero_shot_method.md) ·
[raw summary](../../evidence/claims/claim_6/raw_results.json) ·
[12-row raw ledger](../../evidence/claims/claim_6/zero_shot_rows.json) ·
[B.9 certificate](../../evidence/claims/claim_6/theorem_b9_certificate.json) ·
[checker](../../evidence/claims/claim_6/checker_output.json) ·
[controls](../../evidence/claims/claim_6/negative_control_output.json) ·
[environment](../../evidence/claims/claim_6/run_environment.json) ·
[mechanics code](../../repro/claim6_mechanics.py) ·
[zero-shot code](../../repro/claim6_zeroshot.py)

Run `aa790329-76b1-48a3-a8e7-9e343d6440ba`, Git `16836d4`; estimate 64
scientific cores, provider allocation 8 vCPUs, 64 logical CPUs visible,
593.15 scientific seconds, 610 seconds provider runtime, approximately
`$0.0051` at the catalog rate of `$0.03/hour`.

The superseded parent is labeled **Historical rejected baseline** because its
invented 10× disconnected-square gate is not a Figure 8 quantifier.
