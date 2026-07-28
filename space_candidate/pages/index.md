# Planar Symmetric Pattern Generation — current reproduction

Previous live judged score: **8/12**. Current evidence verdicts:
**Claims 1–5 VERIFIED; Claim 6 BLOCKED**. A projected 10–12/12 range is a
forecast only; no score increase is claimed before a live judge result.

## Current verification

| Claim | Canonical page | Verdict | Strongest evidence |
| --- | --- | --- | --- |
| 1 | [Conjugation](#/claim-1) | VERIFIED | 17/17 subgroup and recovery checks |
| 2 | [Universal approximation](#/claim-2) | VERIFIED | universal symbolic certificate, 3 tamper controls |
| 3 | [Invariant decomposition](#/claim-3) | VERIFIED | 17/17, max `5.34e-16` |
| 4 | [Pattern generation](#/claim-4) | VERIFIED | 17/17, max `1.62e-15` |
| 5 | [VTM connectivity](#/claim-5) | VERIFIED | paper 128², 401.2× separation, flood-fill oracle |
| 6 | [Mechanics and zero-shot](#/claim-6) | BLOCKED | mechanics/B.9 verified; 1/1,000 samples per group |

[Release forecast and limitations](#/release) ·
[illustrated report](../reports/planar-symmetric-pattern-generation/report.md) ·
[tutorial notebook](../notebooks/planar_symmetric_pattern_generation.py) ·
[machine-readable visibility matrix](../evidence/visibility_matrix.json) ·
[fast release checker](../verify_release.py) ·
[fixed full verifier](../reproduce.py) ·
[locked environment](../uv.lock)

Full regeneration command, fixed across every experiment:

```bash
uv run --frozen python reproduce.py
```

Fast published-evidence check:

```bash
uv run --frozen python verify_release.py
```

Both verifiers exit nonzero when required evidence fails. Formal evidence run:
`be3f0b80-0cad-420e-a04b-fbe56ce5c7e5`, Git
`ccf8fe2598f08cf010ed20ea63e266a36b5641b4`, HF `cpu-upgrade`, 64 vCPUs,
official uv Python 3.12 image, Python 3.12.12, deterministic seeds recorded per
claim.

## Visibility matrix

| Claim | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | yes | yes | yes | yes | yes | yes | VERIFIED |
| 3 | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | yes | yes | yes | yes | yes | yes | VERIFIED |
| 5 | yes | yes | yes | yes | yes | yes | VERIFIED |
| 6 | yes | yes | yes | yes | yes | yes | BLOCKED |

## Preserved history

- [Historical rejected baseline — previous verify page](#/verify)
- [Historical rejected baseline — previous overview page](#/overview)

Those pages remain byte-for-byte identical to judged revision `0a5097…`.
Their single-target Claim 2 test and deferred Claim 5 are superseded by the
current pages above; they are not the current verification run.
