# Flat Minima and Generalization — ICML 2026 reproduction

CPU-only, clean-room reproduction for OpenReview `u6zp8zZ8Ou` / arXiv
`2511.03548`. The experiment executes the paper's theorem instances directly:
exact SA-ERM certificates, SA-GD dynamics, full SAM trajectories, stability
scaling, event-frequency checks, and prespecified boundary controls.

```bash
uv venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python repro/src/reproduce_flat_minima.py
.venv/bin/python repro/src/verify_all.py
```

The generated evidence is written to `outputs/full/`.
