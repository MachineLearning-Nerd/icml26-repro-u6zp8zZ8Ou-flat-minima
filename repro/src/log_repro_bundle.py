#!/usr/bin/env python3
"""Register the complete reproduction as a local Trackio Bucket artifact."""

from __future__ import annotations

import json
from pathlib import Path

import trackio


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    run = trackio.init(
        project="flat-minima-sco-repro",
        name="cpu-theorem-instance-reproduction",
        config={
            "openreview_id": "u6zp8zZ8Ou",
            "arxiv_id": "2511.03548",
            "automatic_claims": 3,
            "live_claims": 4,
            "compute": "local CPU only",
            "gpu_used": False,
            "network_calls": 0,
            "saerm_certificate_rows": 576,
            "sagd_suffixes": 1984,
            "sam_full_runs": 80,
            "sam_suffixes": 4800,
        },
        embed=False,
        auto_log_gpu=False,
        auto_log_cpu=False,
    )
    artifact = trackio.Artifact(
        "flat-minima-cpu-reproduction",
        type="dataset",
        description=(
            "Complete CPU-only ICML 2026 theorem-instance reproduction: exact SA-ERM and SA-GD "
            "certificates, full high-dimensional SAM trajectories, all suffix rows, source audit, "
            "boundary controls, tests, environment and hashes."
        ),
        metadata={
            "openreview_id": "u6zp8zZ8Ou",
            "arxiv_id": "2511.03548",
            "paper_pdf_sha256": "47e2027051f0d411a657057374cb9b2095430f8dae0114c13763b04e6d50fa24",
            "gpu_used": False,
            "theorem_instances_not_proxy_tasks": True,
        },
    )
    artifact.add_dir(ROOT / "repro", name="repro")
    artifact.add_dir(ROOT / "outputs" / "full", name="outputs/full")
    artifact.add_dir(ROOT / "source", name="source")
    artifact.add_dir(ROOT / "paper", name="paper")
    logged = trackio.log_artifact(
        artifact,
        aliases=["challenge", "cpu", "theorem-instance", "complete", "reproducible"],
    )
    trackio.finish()
    print(
        json.dumps(
            {
                "qualified_name": logged.qualified_name,
                "size_bytes": logged.size,
                "files": len(logged.manifest or []),
                "run": run.name,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
