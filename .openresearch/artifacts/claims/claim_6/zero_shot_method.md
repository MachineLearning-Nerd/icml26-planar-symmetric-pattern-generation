# Zero-shot first-12 method

Fetch the released p1-only diffusion checkpoint and the exact representation
and diffusion sources from commit
`b6a27efef00b80923ce9e6b66bb8847e83f289cf`; reject every hash mismatch.
The checkpoint must report epoch index 99 and contain no symmetry-label field.

Instantiate each of the paper's first 12 planar groups at 64x64 with the
released 16-level, 2^19-entry hash representation. Run the exact 300-step
AdamW/SDS schedule at seed 42. Twelve four-thread processes run concurrently
on the HF cpu-upgrade allocation. Replay p4mm independently with the same seed.

At deterministic fractional-coordinate queries, compare the optimized field
to independently transcribed crystallographic generators, both continuously
and after binarization. Compute volume error against 0.5 and re-evaluate each
mask with the released p=5 periodic homogenization solver. A p1 output tested
as p4mm and a same-volume disconnected square are intended-failure controls.

The paper reports 1,000 samples per group. This experiment runs one exact
sample per group, so it tests full group coverage and the exact algorithm but
does not reproduce the 12,000-sample diversity distribution.
