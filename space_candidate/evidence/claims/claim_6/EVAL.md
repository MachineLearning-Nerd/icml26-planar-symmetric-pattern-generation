# Claim 6 evaluator note

Verdict: **BLOCKED**.

Two components are VERIFIED: Equation 8 homogenization/adjoint mechanics and
the independently reconstructed Theorem B.9 certificate. The exact released
p1-only checkpoint also completes a 300-step, seed-42 zero-shot replay for one
sample in each of the first 12 groups. That scoped mechanism passes symmetry,
volume, uniqueness, direct equilibrium, void, and deterministic-replay checks.

It is not the paper's 1,000 samples per group. The observed checked worker range
is 506.6–2,335.3 seconds with four threads. On 64 vCPUs, 12,000 checked samples
need at least 750 ideal waves, or 20.27 days at the observed maximum before
overhead. The population-level Figure 8 statement is therefore not verified or
falsified on the authorized CPU campaign.

The released native CG solver reaches residual 0.380 on one generated mask; the
current verifier records it and uses an independent direct sparse solve
(maximum residual `3.25e-9`) instead. The parent route's invented 10×
disconnected-square gate is labeled **Historical rejected baseline**.
