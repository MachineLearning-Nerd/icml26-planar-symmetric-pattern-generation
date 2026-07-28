# Claim 5 evaluator note

Verdict: **VERIFIED** for the stated VTM mechanism.

The exact released finite-element VTM is evaluated at the paper's 128×128 Q1
mesh. A connected p4mm periodic design has zero unreachable material cells and
score `1.9474`; symmetric periodic islands have 1,936 unreachable cells and
score `781.305` (401.2× hotter). Scores are independently recomputed, residuals
are below `4.54e-7`, and one fixed released-adjoint step reduces the island
score by 12.04%. The released 192×192 p6mm configuration independently gives
641.2× separation.

This does not claim reproduction of the SDXL image generator or physical
fabrication; those are recorded deviations rather than hidden substitutions.
