# Claim 2 method

The result is not inferred from a sweep. The verifier checks a proof DAG:
Stone-Weierstrass density, Reynolds contraction, exact Hironaka decomposition,
and the uniform-to-L1 inequality. It also checks the paper’s 17-entry rank
ledger.

Three destructive controls must fail:

- use a pre-averaging tolerance \(2\epsilon/|\Omega|\), which exhausts the
  strict error budget;
- delete the Hironaka free-module step;
- corrupt the `p4gm` module rank.

Exact command: `uv run --frozen python reproduce.py`.

Standalone verifier: `uv run --frozen python repro/claim2_proof.py`.
