# Release forecast and claim summary

Previous live judged score: `8/12`

Conservative projected score range after the proposed change: **10–12/12**

Best-supported possible new score: **12/12 (forecast, not a judge result)**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 2 | 2 | HIGH | VERIFIED | All 17 point groups pass subgroup and conjugation recovery; full-credit regression preserved. |
| 2 | 1 | 2 | MEDIUM | VERIFIED | Universal proof obligations and quantifiers are reconstructed and tamper-tested; residual risk is that the certificate is not checked by a Lean/Coq kernel. |
| 3 | 2 | 2 | HIGH | VERIFIED | All 17 groups pass Equation 3 invariance at `5.34e-16`; intended-failure control is `2.21`. |
| 4 | 2 | 2 | HIGH | VERIFIED | All 17 groups pass Algorithm 1 symmetry at `1.62e-15`; no-projection control is `2.41`. |
| 5 | 0 | 2 | HIGH | VERIFIED | Paper-native 128×128 VTM, flood-fill oracle, 401.2× score separation, residual and adjoint checks, plus released 192×192 replay. |
| 6 | 1 | 2 | MEDIUM | BLOCKED | Homogenization and Theorem B.9 are verified; exact zero-shot mechanism passes for all first 12 groups at one sample each. Paper-scale 1,000/group distribution remains unrun. |

Current total score: **8/12**.

Conservative projected total score range: **10–12/12**.

Best-supported possible total score: **12/12**, only as a forecast.

Claims changed since the previous judge result: Claim 2 replaces a single
p4mm target curve with a universal proof certificate; Claim 5 replaces no
experiment with paper-native VTM evidence; Claim 6 adds exact homogenization,
B.9, and all-12 zero-shot calibration but remains BLOCKED at population scale.

Remaining BLOCKED claim: Claim 6. The paper evaluates 1,000 samples for each of
12 groups. The checked route ran one per group. With 16 concurrent four-thread
workers on 64 vCPUs, 12,000 checked samples require at least 750 waves; the
observed slowest checked worker gives a 20.27-day lower bound before overhead.

All scientific CPU jobs used HF `cpu-upgrade`, the pinned image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`, the one repository `.venv`,
and the exact fixed command `uv run --frozen python reproduce.py`.

Exact publication action after all gates pass: upload only the text paths in
`evidence/upload_allowlist.txt` to the existing Space
`DineshAI/nbU2LNYdZN`, verify the returned revision and every downloaded hash,
then fast-forward the exact published text state to GitHub `main`.
