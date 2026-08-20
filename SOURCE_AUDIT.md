# Source audit

The audit is pinned to the paper source below. The pin makes the claim anchors reproducible; it is not an author endorsement or a claim that the paper’s proofs have been formally verified by a proof assistant.

| Field | Value |
| --- | --- |
| Paper | *Planar Symmetric Pattern Generation* |
| arXiv revision | `2606.02073v1` |
| Source URL | <https://ar5iv.labs.arxiv.org/html/2606.02073> |
| Retrieved | `2026-07-28T17:46:13Z` |
| Pinned source SHA-256 | `0d9de93e9af7441ac803837bf4bebceed7d890b015ea4c194bad5dd414921d55` |
| Pin record | [`.openresearch/source/source_pin.json`](.openresearch/source/source_pin.json) |

Claim anchors from the pinned source:

- C1: Theorem 3.2 (`#S3.Thmtheorem2`)
- C2: Theorem 3.3 (`#S3.Thmtheorem3`)
- C3: Equation 3 (`#S3.E3`)
- C4: Algorithm 1 (`#S3.A1`)
- C5: Equation 6 (`#S5.E6`)
- C6: Equation 8 (`#S5.E8`), Figure 8 (`#S6.F8`), and Theorem B.9 (`#A2.Thmtheorem9`)

The audit preserves the paper’s quantifiers. In particular, C6 is not promoted from a one-sample-per-group mechanism check to the paper-scale statement requiring 1,000 samples per group. The finite 17-group checks for C1, C3, and C4 are explicitly labeled regression evidence rather than replacements for the corresponding abstract theorems.
