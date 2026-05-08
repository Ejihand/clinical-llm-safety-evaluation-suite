"""Build a run manifest for traceability (versions, hashes, git, environment)."""

from __future__ import annotations

import datetime
import hashlib
import json
import platform
import subprocess
import sys
import uuid
from importlib import metadata
from pathlib import Path
from typing import Any

from clinical_llm_safety_eval.evaluation_version import RUBRIC_VERSION, TEST_PACK_VERSION


def _file_sha256(path: Path) -> str:
    """Return hex SHA-256 of file contents."""
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _git_head_and_dirty(project_root: Path) -> tuple[str, bool]:
    """Return (commit_or_unknown, is_dirty). Fails gracefully outside git or in CI."""
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        ).stdout.strip()
        return head, bool(status)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "unknown", False


def _harness_version() -> str:
    try:
        return metadata.version("clinical-llm-safety-eval")
    except metadata.PackageNotFoundError:
        return "0.dev0"


def _resolved_core_deps() -> dict[str, str]:
    """Record versions of pandas/numpy if present (helps reproduce numeric runs)."""
    out: dict[str, str] = {}
    for dist_name in ("pandas", "numpy"):
        try:
            out[dist_name] = metadata.version(dist_name)
        except metadata.PackageNotFoundError:
            pass
    return out


def build_run_manifest(
    *,
    project_root: Path,
    test_cases_path: Path,
    responses_path: Path,
    results_path: Path,
    defect_log_path: Path,
    manifest_path: Path,
    model_id: str | None = None,
    temperature: str | None = None,
) -> dict[str, Any]:
    """Assemble a JSON-serializable manifest for one evaluation run."""
    run_id = str(uuid.uuid4())
    commit, dirty = _git_head_and_dirty(project_root)
    manifest: dict[str, Any] = {
        "run_id": run_id,
        "utc_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "data_classification": "synthetic_public_demo",
        "git_commit": commit,
        "git_dirty": dirty,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "harness_version": _harness_version(),
        "test_pack_version": TEST_PACK_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "dependencies": _resolved_core_deps(),
        "input_hashes": {
            "test_cases_sha256": _file_sha256(test_cases_path),
            "model_responses_sha256": _file_sha256(responses_path),
        },
        "outputs": {
            "evaluation_results": str(results_path.relative_to(project_root)),
            "defect_log": str(defect_log_path.relative_to(project_root)),
            "manifest": str(manifest_path.relative_to(project_root)),
        },
    }
    if model_id is not None:
        manifest["model_id"] = model_id
    if temperature is not None:
        manifest["temperature"] = temperature
    return manifest


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    """Write manifest as pretty-printed JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def load_manifest(path: Path) -> dict[str, Any]:
    """Load manifest JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_footer_markdown(manifest: dict[str, Any]) -> str:
    """Short Markdown block appended to reports."""
    lines = [
        "## Run manifest (reproducibility)",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| run_id | `{manifest.get('run_id', '')}` |",
        f"| utc_timestamp | {manifest.get('utc_timestamp', '')} |",
        f"| harness_version | {manifest.get('harness_version', '')} |",
        f"| test_pack_version | {manifest.get('test_pack_version', '')} |",
        f"| rubric_version | {manifest.get('rubric_version', '')} |",
        f"| git_commit | `{manifest.get('git_commit', '')}` |",
        f"| git_dirty | {manifest.get('git_dirty', '')} |",
        f"| data_classification | {manifest.get('data_classification', '')} |",
    ]
    if manifest.get("model_id"):
        lines.append(f"| model_id | {manifest['model_id']} |")
    if manifest.get("temperature"):
        lines.append(f"| temperature | {manifest['temperature']} |")
    hashes = manifest.get("input_hashes") or {}
    if hashes:
        lines.append(f"| test_cases_sha256 | `{hashes.get('test_cases_sha256', '')[:16]}...` |")
        lines.append(f"| model_responses_sha256 | `{hashes.get('model_responses_sha256', '')[:16]}...` |")
    lines.append("")
    lines.append(
        "Full manifest path: `data/run_manifest.json`. "
        "Automated scores are triage only; they are not a substitute for clinical review."
    )
    return "\n".join(lines)
