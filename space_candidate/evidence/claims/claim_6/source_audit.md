# Claim 6 source audit

Paper source SHA-256:
`0d9de93e9af7441ac803837bf4bebceed7d890b015ea4c194bad5dd414921d55`.

Equation 8 defines the area-normalized effective elastic tensor from three
unit test strains and periodic equilibrium. In 2D the stated bulk quantity
is `c = E11^H + E12^H + E21^H + E22^H`, and Equation 10 minimizes `-c`.
Appendix F.3 fixes plane stress, ν=0.3, E in [1e-6,1], SIMP p=10, Q1
elements, 64x64 during training and 128x128 during testing.

Theorem B.9 universally covers every planar group and every 3D space group.
Its proof reduces maximal finite rational classes to integral classes, covers
the two 2D maximal classes by B2/G2 Weyl actions, covers the three cubic 3D
lattice classes by B3/C3 root or dual actions, invokes Lemma B.7 for the dual,
and then Theorem B.6 for the affine translation lift.

Figure 8 is distinct: a diffusion model trained on 36,000 p1-only 64x64
topology-optimized masks for 100 epochs is used zero-shot with additional
planar-group representations. The paper says 300 AdamW/SDS steps and evaluates
the first 12 planar groups with 1,000 samples per setting.
