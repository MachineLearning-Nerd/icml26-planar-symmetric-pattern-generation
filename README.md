# ICML 2026 — Planar Symmetric Pattern Generation

[![Open in Molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/blob/main/notebooks/planar_symmetric_pattern_generation.py)

Independent claim-by-claim reproduction audit for [arXiv:2606.02073](https://arxiv.org/abs/2606.02073), *Planar Symmetric Pattern Generation*.

The repository was renamed from `icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation` to `icml26-planar-symmetric-pattern-generation` so the public URL describes the paper rather than the challenge identifier.

## Audit status

`PARTIAL_C1_C5_VERIFIED_C6_BLOCKED_MECHANICS_B9_ZERO_SHOT_MECHANISM_VERIFIED_HISTORICAL_SCORE_8_OF_12_NO_CURRENT_SCORE`

Claims 1–5 are verified within the finite or symbolic scopes documented below. Claim 6 has verified homogenization, Theorem B.9, and zero-shot mechanism checks, but remains blocked for the paper-scale zero-shot quantifier: the audit ran one sample per group while the paper reports 1,000. The historical 8/12 judge result is preserved; the 10–12/12 values are forecasts only. There is no current judge score claim and no author endorsement claim.

The maintained dossier is [`STATUS.md`](STATUS.md), with claim production paths in [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md), source pins in [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md), environment details in [`ENVIRONMENT.md`](ENVIRONMENT.md), and a machine-checkable final audit in [`verify_final.py`](verify_final.py).

## What the paper does

The paper proposes a symmetrization framework for arbitrary planar groups. It transforms a continuous 2D representation into one that respects a selected planar symmetry while preserving continuity, develops an approximation argument for symmetric functions, and applies the construction to visual and material-design tasks.

The audit covers six claims:

1. planar groups can be conjugated into reflection groups;
2. the symmetric representation has universal approximation capability;
3. the paper’s Equation 3 decomposition is invariant;
4. Algorithm 1 generates patterns for all 17 listed planar groups;
5. the Virtual Temperature Method (VTM) penalizes disconnected material;
6. the mechanics, 3D theorem, and zero-shot metamaterial evaluation hold at the paper’s stated scale.

## Claim and evidence ledger

Claims 1–5 are currently `VERIFIED`. Claim 6 is intentionally `BLOCKED`: its mechanics and Theorem B.9 components pass, and the zero-shot mechanism was calibrated for the first 12 groups, but the paper-scale evaluation requires 1,000 samples per setting and only one sample per group was run.

| Claim | Paper anchor | How the claim is produced and checked | Current assessment |
|---|---|---|---|
| 1 | Theorem 3.2 — conjugation into reflection groups | [`repro/baseline.py`](repro/baseline.py) checks all 17 paper-listed planar groups, subgroup membership, distorted/inverse-conjugated recovery, and a rejected (p6<D4) control | `VERIFIED`, high confidence for the finite catalogue; not a proof-kernel replacement for the abstract theorem |
| 2 | Theorem 3.3 and Appendix C.4 — universal symmetric approximation | [`repro/claim2_proof.py`](repro/claim2_proof.py) checks quantifier order, (L^1) error, compact-domain density, Reynolds contraction, Hironaka module decomposition, and strict error budget; tamper controls fail | `VERIFIED`, medium confidence; independent symbolic certificate, not Lean/Coq formalization |
| 3 | Equation 3 — invariant decomposition | [`repro/baseline.py`](repro/baseline.py) evaluates all 17 groups and rejects a non-invariant coefficient control | `VERIFIED`, high confidence; maximum residual (5.34\times10^{-16}) |
| 4 | Algorithm 1 and Section 6.1 — all-group pattern generation | [`repro/baseline.py`](repro/baseline.py) projects into asymmetric units and checks symmetry residuals for all 17 groups; a no-projection mutation fails | `VERIFIED`, high confidence for the symmetry contract; does not evaluate image aesthetics or prompt adherence |
| 5 | Equation 6, Figure 4, Appendix E.3/F.2 — VTM connectivity | [`repro/claim5_vtm.py`](repro/claim5_vtm.py) runs the released finite-element VTM on the paper’s 128×128 p4mm mesh, independently recomputes scores and flood-fill reachability, and checks a 192×192 p6mm configuration | `VERIFIED`, high confidence for the connectivity mechanism; does not establish SDXL generation or fabrication outcomes |
| 6 | Equation 8, Theorem B.9, Figure 8, Section 6.4 — mechanics, 3D classes, zero-shot evaluation | [`repro/claim6_mechanics.py`](repro/claim6_mechanics.py) checks homogenization/adjoints/B.9; [`repro/claim6_zeroshot.py`](repro/claim6_zeroshot.py) runs the exact 300-step p1-only replay for the first 12 groups and records scope | `BLOCKED`, medium confidence: mechanics and B.9 verified, but 1/1,000 samples per group is not sufficient for the bundled evaluation claim |

### Common evidence path

Every claim follows this chain:

`paper anchor → exact claim contract → executable checker/certificate → negative control → raw evidence → release verifier → report`

Run the cumulative audit with:

```bash
uv run --frozen python reproduce.py
```

The evaluator-facing contracts, methods, controls, and raw outputs are under [`space_candidate`](space_candidate); the illustrated synthesis is [`reports/planar-symmetric-pattern-generation/report.md`](reports/planar-symmetric-pattern-generation/report.md). `verify_release.py` checks that the published evidence package and historical protections are complete.

## Key evidence

| Result | Recorded evidence |
|---|---|
| Claims 1 and 3 | 17/17 planar groups; maximum subgroup/invariance residuals at numerical precision |
| Claim 2 | 11 proof obligations and 3 independent tamper controls pass |
| Claim 4 | 17/17 Algorithm 1 symmetry checks; no-projection control fails as intended |
| Claim 5 | On 128×128 p4mm, connected VTM score 1.9474 vs island score 781.3051 — a 401.2× separation; flood fill finds 0 vs 1,936 unreachable material cells |
| Claim 6 mechanics | Full-solid homogenization 2.857142857 at 64² and 128²; released adjoint finite-difference error 0.049%; Theorem B.9 9/9 obligations and 3/3 controls |
| Claim 6 zero-shot scope | First 12 groups: 12 distinct masks, 1.2126% volume MAE, 0.2225% maximum binary mismatch, and direct equilibrium residual (3.25\times10^{-9}); paper-scale 1,000/group evaluation remains unrun |

The previous live judged score recorded by the repository is `8/12`. The 10–12/12 value in the reports is a forecast, not a new judge result.

## Reproduce locally

Dependencies are pinned by [`pyproject.toml`](pyproject.toml) and [`uv.lock`](uv.lock). No GPU is required for the documented commands.

```bash
uv sync --frozen
uv run --frozen python reproduce.py
uv run --frozen python verify_release.py
marimo edit notebooks/planar_symmetric_pattern_generation.py
```

Long or uncertain checks used Hugging Face `cpu-upgrade`; the provider allocation and visible CPU metadata are recorded explicitly in the claim pages and command ledger. The notebook embeds evidence and does not rerun the expensive zero-shot campaign by default.

## Branch map

The live branch names describe their evidence role:

| Branch family | Purpose |
|---|---|
| [`historical/judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/historical/judged-baseline) | Preserve the validated 8/12 judged baseline |
| [`audit/c2-universal-approximation`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/audit/c2-universal-approximation) | Symbolic universal-approximation certificate and tamper controls |
| [`audit/c5-vtm-128`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/audit/c5-vtm-128) | Paper-native 128×128 VTM and connectivity oracle |
| [`audit/c5-vtm-192`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/audit/c5-vtm-192) | Released 192×192 p6mm VTM replay |
| [`audit/c6-mechanics-b9`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/audit/c6-mechanics-b9) | Homogenization, adjoint, mesh, and Theorem B.9 checks |
| [`historical/c6-first-12-control`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/historical/c6-first-12-control) | Retain the rejected zero-shot control route for provenance |
| [`audit/c6-zero-shot-scope`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/audit/c6-zero-shot-scope) | Source-faithful first-12-group zero-shot calibration and scope blocker |
| [`release/evaluator-candidate`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/release/evaluator-candidate) | Cumulative evaluator-visible release candidate |
| [`audit/provider-cpu-metadata`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/audit/provider-cpu-metadata) | Correct provider-allocation versus visible-CPU metadata |
| [`release/canonical-upload-fix`](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation/tree/release/canonical-upload-fix) | Canonical index and upload allowlist release fix |

[`branch-audit.md`](branch-audit.md) records the exact old-to-new mapping and the claim lineage for every branch.

## Repository contents

- `repro/` — baseline symmetry checks, universal-approximation certificate, VTM, mechanics, and zero-shot replay.
- `space_candidate/` — evaluator-facing pages, claim contracts, raw evidence, controls, release manifest, and mirrored report.
- `reports/` — illustrated technical report and figures.
- `notebooks/` — interactive evidence-first tutorial.
- `scripts/` — publication, secret-scan, manifest, and blind-review checks.

## Scope and limitations

- The finite 17-group catalogue is deterministic regression evidence and does not replace the abstract group theorem.
- The universal-approximation certificate is independently reconstructed, not a proof-assistant kernel artifact.
- VTM evidence establishes the connectivity mechanism on pinned symmetric test fields; it does not establish visual-generation quality or physical fabrication.
- Claim 6 remains blocked at the stated paper-scale zero-shot quantifier: 12 checked samples are not 12,000.
- Historical score records and rejected routes are preserved for provenance and must not be presented as fresh judge results.

## Citation

```bibtex
@misc{lin2026planar,
  title         = {Planar Symmetric Pattern Generation},
  author        = {Lin, Ning and Chen, Luxi and Chen, Huaguan and Cen, Jiacheng and Li, Chongxuan and Huang, Wenbing and Sun, Hao},
  year          = {2026},
  eprint        = {2606.02073},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2606.02073}
}
```

## Thank you

Thank you to Ning Lin, Luxi Chen, Huaguan Chen, Jiacheng Cen, Chongxuan Li, Wenbing Huang, and Hao Sun for developing a practical and mathematically grounded approach to planar symmetry control across visual and material-design settings. This independent audit is intended to make the assumptions, mechanisms, and evidence boundaries easier to inspect and reproduce.

## Attribution

Repository maintenance commits in the cleaned branch histories use:

`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`

The paper and its authors remain the source of the research claims; this repository contains an independent reproduction and audit record.
