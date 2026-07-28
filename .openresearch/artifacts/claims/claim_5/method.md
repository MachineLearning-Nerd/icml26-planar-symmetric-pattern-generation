# Claim 5 method

Construct one 96x96 p6mm unit cell and tile it into the required 2x2,
192x192 supercell used by the released paper-cutting entrypoint. The positive
design is a fully conducting p6mm sheet connected to Γ. The negative design
contains four periodic hexagonal islands separated by low-conductivity
material. Both are closed under the exact D6 action on the discrete oblique
torus and are exactly periodic.

Run the authors' `ObliqueElemVTM` Q1 finite-element solver at its pinned
release commit. Independently recompute Equation 6 from nodal temperatures,
check the free-DOF residual of the assembled heat equation, and apply a
four-neighbour flood fill from the exact Γ segments. Backpropagate through
the released custom adjoint and apply one predeclared step of size 0.01.

The checker exits nonzero if any exact-symmetry, periodicity, connectivity,
temperature-separation, residual, score-recomputation, descent, or negative
control gate fails.
