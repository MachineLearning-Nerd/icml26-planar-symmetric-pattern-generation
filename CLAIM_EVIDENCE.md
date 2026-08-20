# Claim-to-evidence ledger

This ledger separates what the paper claims, what the repository executes, and what the current evidence actually supports.

| Claim | Paper anchor | How the result is produced | Evidence and controls | Verdict |
| --- | --- | --- | --- | --- |
| C1 — every listed planar group is conjugate into a reflection group | Theorem 3.2 | [`repro/baseline.py`](repro/baseline.py) enumerates the 17 paper-listed groups, checks subgroup membership, and recovers distorted and inverse-conjugated representations | 17/17 groups pass; the rejected `p6<D4` control remains negative | `VERIFIED_SCOPED_HIGH` |
| C2 — universal approximation of continuous invariant functions | Theorem 3.3 and Appendix C.4 | [`repro/claim2_proof.py`](repro/claim2_proof.py) checks quantifier order, compact-domain density, Reynolds contraction, Hironaka-module decomposition, and a strict L1 error budget | 11 proof obligations and three independent tamper controls pass; `upper_bound=0.0625 < epsilon=0.125` | `VERIFIED_SCOPED_MEDIUM` |
| C3 — the Equation 3 decomposition is invariant | Equation 3 | [`repro/baseline.py`](repro/baseline.py) evaluates the decomposition under each group action | 17/17 groups pass; maximum invariance error `5.342948306008566e-16`; non-invariant coefficient control fails | `VERIFIED_SCOPED_HIGH` |
| C4 — Algorithm 1 generates group-symmetric patterns | Algorithm 1 and Section 6.1 | [`repro/baseline.py`](repro/baseline.py) projects into asymmetric units and compares transformed outputs | 17/17 groups pass; maximum symmetry error `1.6237011735142914e-15`; no-projection mutation fails | `VERIFIED_SCOPED_HIGH` |
| C5 — VTM penalizes disconnected material | Equation 6, Figure 4, Appendix E.3/F.2 | [`repro/claim5_vtm.py`](repro/claim5_vtm.py) runs the paper-native VTM, independently recomputes scores, flood-fills material, and checks a released configuration | 128×128 p4mm score ratio `401.2017×`; connected unreachable cells `0` versus island `1936`; 192×192 p6mm ratio `641.2206×` | `VERIFIED_SCOPED_HIGH` |
| C6 — mechanics, Theorem B.9, and paper-scale zero-shot evaluation | Equation 8, Figure 8, Section 6.4, Theorem B.9 | [`repro/claim6_mechanics.py`](repro/claim6_mechanics.py) checks homogenization, adjoints, and B.9; [`repro/claim6_zeroshot.py`](repro/claim6_zeroshot.py) runs the first-12-group mechanism | Mechanics and B.9 pass; zero-shot run has 12 groups × 1 sample, 300 steps, 64×64, seed 42, 12 unique masks, volume MAE `0.01212565`, maximum direct residual `3.25e-9`; paper quantifier is 1,000 samples/group | `BLOCKED_PAPER_SCALE` |

The common production path is:

`paper anchor → exact claim contract → executable producer → independent checker → negative control → raw JSON → release verifier → report`

The canonical evaluator-facing copies are under [`space_candidate`](space_candidate), while protected source and internal artifact copies are under [`.openresearch`](.openresearch). The historical zero-shot control branch is retained for provenance and is not the current verifier.
