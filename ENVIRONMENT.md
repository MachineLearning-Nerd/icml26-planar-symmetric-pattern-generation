# Reproduction environment

The scientific evidence in this repository records the following pinned environment:

- Command: `uv run --frozen python reproduce.py`
- Python: `3.12.12`
- Dependency environment: repository `.venv` resolved from [`uv.lock`](uv.lock)
- Container: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Backend: Hugging Face `cpu-upgrade`
- Provider allocation: 8 vCPUs and 32 GB RAM
- Container-visible logical CPUs: 64
- Project requirements: Python `3.12.*`, CPU PyTorch `2.7.1`, NumPy `1.26.4`, SciPy `1.15.3`, and pinned supporting packages in [`pyproject.toml`](pyproject.toml)

Selected recorded runtimes:

| Workload | Scientific runtime |
| --- | ---: |
| C5 paper 128×128 p4mm | 41.0744 s |
| C5 released 192×192 p6mm | 50.235 s |
| C6 homogenization | 150.005 s |
| C6 first-12 zero-shot mechanism | 593.1547 s |

The provider allocation and the logical CPUs visible inside the accepted container are recorded separately because they differ. The zero-shot run observed 12 concurrent primary workers; extrapolating its slowest worker to 12,000 samples gives a lower bound of 6.09 days before overhead. This is why C6 remains blocked rather than silently rerun or extrapolated.

The repository’s original release verifier is [`verify_release.py`](verify_release.py). The documentation/provenance verifier added for this cleanup is [`verify_final.py`](verify_final.py). No full scientific rerun is claimed by the cleanup commit.
