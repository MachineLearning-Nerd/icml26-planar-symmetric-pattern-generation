# Claim 5 limitations and deviations

This is a direct finite-element VTM and connectivity robustness verification
at the released entrypoint's mesh, not a graph proxy. The release uses
192x192/SIMP=4 while Appendix F.2 says 128x128/SIMP=5; the other sibling
tests the paper-prose configuration. The input densities are deterministic
constructed p6mm designs rather than samples produced by the paper's
diffusion-guided image optimizer. The experiment therefore tests the VTM
mechanism, adjoint, symmetry preservation, and the stated connectivity
premises; it does not reproduce image semantics, fabrication, or prove
optimizer convergence for every initialization.
