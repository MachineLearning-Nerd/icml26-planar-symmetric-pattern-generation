# Claim 5 source audit

Retrieved `https://ar5iv.labs.arxiv.org/html/2606.02073` with an explicit
browser User-Agent on 2026-07-28. SHA-256:
`0d9de93e9af7441ac803837bf4bebceed7d890b015ea4c194bad5dd414921d55`.

Section 6.2 and Equation 6 define a Poisson heat-conduction system in which
solid material conducts and generates heat, void acts as an insulator, and
the p-norm of temperature is minimized. Figure 4 says disconnected solid
islands accumulate heat. The periodic-connectivity argument uses a 2x2
supercell and requires every connected component to meet the sink boundary.
Appendix F.2 fixes Γ, the 128x128 Q1 mesh, q0 in [1e-8, 1e-4],
conductivity in [1e-4, 1], SIMP penalty 5, p=20, and 2x2 Gauss quadrature.

This experiment uses q0=1e-4 and all other stated fixed settings. It binds
the released solver to upstream commit
`b6a27efef00b80923ce9e6b66bb8847e83f289cf` by source-file hashes.
