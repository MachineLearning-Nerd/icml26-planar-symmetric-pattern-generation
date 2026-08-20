# Reproduction report

## Result

Claims 1–5 are supported within their stated finite or symbolic scopes. Claim 6 is mixed: homogenization, adjoint checks, Theorem B.9, and the exact zero-shot mechanism pass for the first 12 groups, but the paper-scale evaluation remains blocked because the audit checked one sample per group instead of 1,000.

## What the paper does

The paper constructs symmetry-controlled planar representations, proves an approximation route for symmetric functions, generates patterns across the 17 wallpaper groups, adds a Virtual Temperature Method for connectivity, and evaluates mechanics and zero-shot metamaterial behavior.

## Evidence highlights

- 17/17 listed planar groups pass the C1 subgroup/conjugation checks.
- C2’s 11 reconstructed proof obligations and strict L1 budget pass, with tamper controls.
- C3 and C4 pass all 17 groups at numerical precision, with intended-failure controls.
- C5 shows a `401.2017×` connected-versus-island VTM score separation on the paper-native 128×128 p4mm configuration and `641.2206×` on the released 192×192 p6mm replay.
- C6 verifies the full-solid homogenization value, the adjoint check, 9/9 Theorem B.9 obligations, and a first-12-group mechanism replay.

## Reproduction boundary

The historical live score is `8/12`. The release report’s `10–12/12` values are forecasts only. No current judge score is asserted, and the repository does not claim author endorsement. The main unresolved scientific gate is the 12,000-sample C6 zero-shot quantifier.
