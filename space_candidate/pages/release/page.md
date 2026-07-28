# Release forecast, visibility, and limitations

Previous live judged score: `8/12`.

Conservative projected range: **10–12/12**.

Best-supported possible score: **12/12 (forecast only)**.

The full confidence table, changed-claim summary, remaining Claim 6 risk, and
exact publication action are in the
[release report](../../evidence/release_report.md). The machine-readable
[visibility matrix](../../evidence/visibility_matrix.json) has no missing
required cells. The [campaign command ledger](../../evidence/campaign_command_ledger.md)
records every material source, execution, audit, and publication command.

Claim 6 is BLOCKED, not silently passed: the paper reports 1,000 generated
samples for each of 12 groups; this CPU campaign ran one exact 300-step sample
per group. Homogenization, Theorem B.9, and the scoped all-group zero-shot
mechanism are separately exposed on [Claim 6](#/claim-6).

The exact judged revision is immutable and its old pages remain under
**Historical rejected baseline**. The current verifier is
[`verify_release.py`](../../verify_release.py), and full evidence regeneration
uses `uv run --frozen python reproduce.py`.
