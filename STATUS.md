# Reproduction status

Repository: [MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation)

Paper: [Planar Symmetric Pattern Generation](https://arxiv.org/abs/2606.02073), arXiv:2606.02073v1.

Overall status:

`PARTIAL_C1_C5_VERIFIED_C6_BLOCKED_MECHANICS_B9_ZERO_SHOT_MECHANISM_VERIFIED_HISTORICAL_SCORE_8_OF_12_NO_CURRENT_SCORE`

| Claim | Status | Confidence and boundary |
| --- | --- | --- |
| C1 — planar groups conjugate into reflection groups | `VERIFIED_SCOPED_HIGH` | All 17 paper-listed groups pass finite subgroup and conjugation-recovery checks; this is regression evidence, not a proof-kernel formalization. |
| C2 — universal approximation for symmetric functions | `VERIFIED_SCOPED_MEDIUM` | Eleven proof obligations, quantifier checks, strict L1 budget, and tamper controls pass; the certificate is independently reconstructed, not Lean/Coq-checked. |
| C3 — Equation 3 invariant decomposition | `VERIFIED_SCOPED_HIGH` | All 17 groups pass with maximum residual `5.342948306008566e-16`; the intended non-invariant control fails. |
| C4 — Algorithm 1 generates all listed group patterns | `VERIFIED_SCOPED_HIGH` | All 17 groups pass with maximum symmetry error `1.6237011735142914e-15`; the no-projection mutation fails. |
| C5 — VTM connectivity mechanism | `VERIFIED_SCOPED_HIGH` | Paper-native 128×128 p4mm and released 192×192 p6mm checks pass, including score recomputation, residuals, symmetry, and flood-fill connectivity. |
| C6 — mechanics, Theorem B.9, and zero-shot evaluation | `BLOCKED_PAPER_SCALE` | Homogenization, adjoints, B.9, and the exact first-12-group mechanism pass, but the run has 1 sample per group versus the paper’s 1,000. |

Historical result: `8/12` live judged score. The report’s `10–12/12` values are forecasts, not current judge results. `current_score_claim=false`, `publication_allowed=false`, and `official_author_endorsement=false`.

The exact claim-to-evidence mapping is in [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md). Run the lightweight repository audit with:

```bash
python3 verify_final.py
```

The original scientific verifier remains [`verify_release.py`](verify_release.py); no full rerun is implied by this documentation update.

Recovery bundle before attribution normalization: `/tmp/icml-planar-before-normalization.B9KyXX/icml-planar-before-normalization.bundle` (SHA-256 `4dc52f4cbdf0a6e6049dc7268862db08d0766478c312c5c65892f039dc00dbf7`).
