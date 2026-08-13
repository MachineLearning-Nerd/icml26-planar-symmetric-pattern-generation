# Branch audit

Repository: [MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation](https://github.com/MachineLearning-Nerd/icml26-planar-symmetric-pattern-generation)

The repository was renamed from `icml26-repro-nbU2LNYdZN-planar-symmetric-pattern-generation`. Former `orx/*` labels are replaced with names that describe the evidence role.

## Old-to-new mapping

| Former branch | Clean branch | Role in the evidence lineage |
|---|---|---|
| `orx/validated-8-of-12-judged-baseline` | `historical/judged-baseline` | Preserve the validated 8/12 judged baseline |
| `orx/claim-2-symbolic-density-certificate` | `audit/c2-universal-approximation` | Universal approximation certificate and tamper controls |
| `orx/claim-5-paper-128-vtm` | `audit/c5-vtm-128` | Paper-native 128×128 VTM and connectivity oracle |
| `orx/claim-5-released-192-vtm` | `audit/c5-vtm-192` | Released 192×192 p6mm VTM replay |
| `orx/claim-6-homogenization-mechanics` | `audit/c6-mechanics-b9` | Homogenization, adjoint, mesh, and Theorem B.9 checks |
| `orx/claim-6-zero-shot-first-12-groups` | `historical/c6-first-12-control` | Rejected zero-shot control route retained for provenance |
| `orx/claim-6-zero-shot-source-faithful-verifier` | `audit/c6-zero-shot-scope` | Source-faithful first-12-group zero-shot calibration and blocker |
| `orx/cumulative-evaluator-visible-release-candidate` | `release/evaluator-candidate` | Cumulative evaluator-visible release candidate |
| `orx/provider-allocated-cpu-metadata-correction` | `audit/provider-cpu-metadata` | Provider allocation versus visible-CPU metadata correction |
| `orx/canonical-index-upload-allowlist-fix` | `release/canonical-upload-fix` | Canonical index and upload allowlist release fix |

`main` is the canonical publication surface. The former `orx/*` remote branches are deleted after the clean replacements are pushed; reachable evidence content is retained in the corresponding histories.

## Claim lineage

| Claim | Primary branch evidence | Canonical files |
|---|---|---|
| 1 — group conjugation | historical baseline | `repro/baseline.py`, `space_candidate/pages/claim-1/` |
| 2 — universal approximation | `audit/c2-universal-approximation` | `repro/claim2_proof.py`, `space_candidate/pages/claim-2/` |
| 3 — invariant decomposition | historical baseline | `repro/baseline.py`, `space_candidate/pages/claim-3/` |
| 4 — all-group pattern generation | historical baseline | `repro/baseline.py`, `space_candidate/pages/claim-4/` |
| 5 — VTM connectivity | `audit/c5-vtm-128`, `audit/c5-vtm-192` | `repro/claim5_vtm.py`, `space_candidate/pages/claim-5/` |
| 6 — mechanics, B.9, zero-shot | `audit/c6-mechanics-b9`, `audit/c6-zero-shot-scope` | `repro/claim6_mechanics.py`, `repro/claim6_zeroshot.py`, `space_candidate/pages/claim-6/` |

## Attribution and verification policy

- Clean maintenance commits use `MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>`.
- Branch cleanup changes labels and links, not the scientific evidence or its limitations.
- The rejected zero-shot control is historical; it is not the current verifier.
- Claim 6 remains blocked until the paper-scale sampling quantifier is actually run or formally narrowed.
- Release branches are candidate publication surfaces until the external evaluator runs them.
