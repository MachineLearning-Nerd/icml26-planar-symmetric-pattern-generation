# Reproduction command ledger

This ledger records the material commands used to retrieve, execute, verify,
and release the evidence. Read-only inspection commands (`sed`, `rg`, and JSON
formatting) are omitted because they do not alter or generate scientific
evidence. No credential-bearing command is recorded.

## Source and startup

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 4e5aa507-319b-4d9c-b9dd-ef10beda6e9f
curl --user-agent "OpenResearch reproduction audit/1.0" https://ar5iv.labs.arxiv.org/html/2606.02073
git clone https://huggingface.co/spaces/DineshAI/nbU2LNYdZN
git -C <judged-space-clone> checkout 0a5097dafd70804544be18562cbdafe265bf4617
git clone https://huggingface.co/spaces/ProCreations/repro-planar-symmetric-pattern-generation
```

The paper bytes were hashed with `sha256sum`; the exact judged Space tree was
hashed into `.openresearch/protected/judged_space_manifest.sha256`.

## Fixed scientific command

Every experiment node inherited exactly:

```bash
uv run --frozen python reproduce.py
```

Every nontrivial or uncertain CPU run used:

```bash
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade
orx exp wait <experiment-id> --timeout 480
orx logs <run-id>
```

No GPU command was issued. Hyperparameters and claim stages were committed in
code or `campaign_config.json`, never injected through an alternate command.

## Release-gate commands

```bash
uv run --frozen python verify_release.py
marimo check --strict notebooks/planar_symmetric_pattern_generation.py
uv run --frozen python scripts/audit_protected_space.py
uv run --frozen python scripts/evaluator_blind_review.py --pass-name prepublication-pass-1 --reset
uv run --frozen python scripts/evaluator_blind_review.py --pass-name post-fix-pass-2
uv run --frozen python scripts/build_space_release_manifest.py
uv run --frozen python scripts/scan_space_secrets.py
.venv/bin/python space_candidate/verify_release.py
```

## Publication and post-publication commands

These commands are executed only after the cumulative HF run and every
release gate succeed:

```bash
/opt/homebrew/bin/python3 scripts/publish_space_text.py --expected-parent 0a5097dafd70804544be18562cbdafe265bf4617
/opt/homebrew/bin/python3 scripts/verify_published_space.py --revision <returned-revision> --output <fresh-empty-directory>
uv run --frozen python scripts/evaluator_blind_review.py --source <fresh-download> --output <fresh-download>/postpublication_evaluator_review.json --pass-name postpublication --reset
git push origin <winning-release-sha>:main
git ls-remote origin refs/heads/main
```

The publication helper reads the existing authenticated Hugging Face session;
it never prints or writes token values.
