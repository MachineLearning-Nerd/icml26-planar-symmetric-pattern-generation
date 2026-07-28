# Claim 6 mechanics and theorem method

Fetch the authors' `fea_base.py` and `struct.py` from immutable commit
`b6a27efef00b80923ce9e6b66bb8847e83f289cf`, reject hash mismatches, and run
the native three-load-case periodic solver.

Calibrate full material at both meshes against `2/(1-nu)`; independently
recompute element energy and all three reduced-system residuals. Starting
from a smooth p4mm density of fixed mean, project the native adjoint into the
zero-mean p4mm subspace. A predeclared central difference checks the derivative;
the positive step must improve normalized bulk modulus, the opposite step must
worsen it, and a doubled 128x128 replay must be mesh-consistent.

Theorem B.9 is checked separately by an explicit proof DAG and full low-
dimensional maximal-class ledger. Deleting the dual cubic class, changing a
maximal order, or making the invariant bilinear form singular must be rejected.
