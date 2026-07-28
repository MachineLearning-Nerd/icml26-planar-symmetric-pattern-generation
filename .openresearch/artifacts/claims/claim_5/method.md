# Claim 5 method

Construct one 64x64 p4mm unit cell and tile it into the required 2x2,
128x128 supercell. The positive design is a periodic cross network connected
to Γ. The negative design contains four periodic square islands separated by
low-conductivity material. Both are exactly D4-invariant and periodic.

Run the authors' `ObliqueElemVTM` Q1 finite-element solver at its pinned
release commit. Independently recompute Equation 6 from nodal temperatures,
check the free-DOF residual of the assembled heat equation, and apply a
four-neighbour flood fill from the exact Γ segments. Backpropagate through
the released custom adjoint and apply one predeclared step of size 0.01.

The checker exits nonzero if any exact-symmetry, periodicity, connectivity,
temperature-separation, residual, score-recomputation, descent, or negative
control gate fails.
