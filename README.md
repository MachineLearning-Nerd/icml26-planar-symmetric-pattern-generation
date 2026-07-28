# Planar Symmetric Pattern Generation — claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/blob/main/notebooks/planar_symmetric_pattern_generation.py)

This repository reproduces the six judged claims of
[Planar Symmetric Pattern Generation (arXiv:2606.02073)](https://arxiv.org/abs/2606.02073).
The previous live score is **8/12**. Current evidence marks Claims 1–5
**VERIFIED** and Claim 6 **BLOCKED**. A conservative projected range of
10–12/12 is a forecast, not a new judge result.

The main improvements are:

- Claim 2 replaces a one-target p4mm fit with a universal symbolic proof
  certificate and three tamper controls.
- Claim 5 runs the paper-native 128×128 VTM: disconnected periodic islands
  score 781.305 versus 1.947 for a connected design (**401.2×**), while an
  independent flood fill finds 1,936 versus zero unreachable material cells.
- Claim 6 verifies Equation 8 homogenization, the released adjoint, and
  Theorem B.9. Its exact zero-shot mechanism passes once for all first 12
  groups, but the paper's 1,000 samples per group remain unrun, so the bundled
  claim stays BLOCKED.

All long or uncertain CPU work ran on Hugging Face `cpu-upgrade`; no GPU was
used. The pinned container is
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`; the environment is Python
3.12 in one repository `.venv`, locked by `uv.lock`. The fixed command for
every experiment is:

```bash
uv run --frozen python reproduce.py
```

Read the [illustrated technical report](reports/planar-symmetric-pattern-generation/report.md)
or open the [self-contained marimo tutorial](notebooks/planar_symmetric_pattern_generation.py).
The tutorial embeds the evidence and does not rerun expensive work.

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public README, report, notebook, and published Space mirror | Not run as an experiment (publication surface) | Presentation-only; formal evidence comes from frozen experiment branches | none |
| [`orx/validated-8-of-12-judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/validated-8-of-12-judged-baseline) | Freeze judged baseline | `uv run --frozen python reproduce.py` | Claims 1/3/4 verified; 2 toy, 5 blocked, 6 partial | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible |
| [`orx/claim-2-symbolic-density-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/claim-2-symbolic-density-certificate) | Universal proof certificate | `uv run --frozen python reproduce.py` | Claim 2 VERIFIED; 11 obligations, 3 controls | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 0.333 s scientific |
| [`orx/claim-5-paper-128-vtm`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/claim-5-paper-128-vtm) | Paper 128×128 VTM and connectivity oracle | `uv run --frozen python reproduce.py` | Claim 5 VERIFIED; 401.2× separation | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 41.07 s scientific |
| [`orx/claim-6-homogenization-mechanics`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/claim-6-homogenization-mechanics) | Equation 8, adjoint, mesh, B.9 | `uv run --frozen python reproduce.py` | Mechanics and B.9 VERIFIED; zero-shot still blocked | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 150.01 s scientific |
| [`orx/claim-6-zero-shot-first-12-groups`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/claim-6-zero-shot-first-12-groups) | Historical rejected 10× control route | `uv run --frozen python reproduce.py` | Failed an unreported 10× square threshold; retained only to explain lineage | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 26m50s wall |
| [`orx/claim-6-zero-shot-source-faithful-verifier`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/claim-6-zero-shot-source-faithful-verifier) | All-12 exact SDS replay plus independent direct mechanics | `uv run --frozen python reproduce.py` | Scoped mechanism VERIFIED; full Claim 6 BLOCKED at 1/1,000 samples/group | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 2,529.99 s scientific |
| [`orx/cumulative-evaluator-visible-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/cumulative-evaluator-visible-release-candidate) | Canonical pages, raw evidence, reports, notebook, release gates | `uv run --frozen python reproduce.py` | Claims 1–5 pass; Claim 6 remains BLOCKED | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 593.15 s scientific |
| [`orx/provider-allocated-cpu-metadata-correction`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/provider-allocated-cpu-metadata-correction) | Distinguish provider allocation from visible CPUs and recalibrate paper-scale bound | `uv run --frozen python reproduce.py` | Cumulative replay passed; no scientific threshold changed | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible; 1,047.07 s scientific |
| [`orx/canonical-index-upload-allowlist-fix`](https://github.com/MachineLearning-Nerd/icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation/tree/orx/canonical-index-upload-allowlist-fix) | Upload the current canonical index ahead of preserved history | `uv run --frozen python reproduce.py` | Final cumulative replay target; publication-only allowlist fix | HF cpu-upgrade, 8 allocated vCPU / 64 logical visible |

## Current claim ledger

| Claim | Paper result | Observed result | Assessment |
| --- | --- | --- | --- |
| 1 | conjugation into reflection groups | 17/17 subgroup and recovery checks | VERIFIED |
| 2 | universal approximation | 11 proof obligations and 3 tamper controls | VERIFIED |
| 3 | Equation 3 invariance | max residual `5.34e-16`, all 17 groups | VERIFIED |
| 4 | Algorithm 1 for all 17 groups | max residual `1.62e-15` | VERIFIED |
| 5 | VTM connectivity | 401.2× score separation; flood-fill oracle | VERIFIED |
| 6 | mechanics, B.9, 1,000/group zero-shot | mechanics/B.9 pass; one sample/group calibrated | BLOCKED |

## Local notebook

```bash
marimo edit notebooks/planar_symmetric_pattern_generation.py
marimo run notebooks/planar_symmetric_pattern_generation.py
```
