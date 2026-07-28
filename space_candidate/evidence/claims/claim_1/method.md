# Claim 1 method

The verifier enumerates one finite point-group representative for each of all
17 wallpaper classes. It independently constructs cyclic and dihedral matrix
groups, checks inclusion in \(D_2\), \(D_4\), or \(D_6\), applies a seeded
well-conditioned invertible matrix, and verifies recovery by its inverse.

Negative control: the sixfold rotation group must not be accepted as a
subgroup of \(D_4\). Seed: `20260728`.
