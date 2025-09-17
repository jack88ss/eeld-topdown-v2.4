"""Utility script to trigger individual workflow tasks based on state/STATUS.yaml.

This is a lightweight scaffold so contributors can extend orchestration without
editing the main automation files. For now it simply parses the manifest and
prints the tasks that are ready to run; teams can adapt it to launch agents
or shell commands asynchronously.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml

MANIFEST = Path("state/STATUS.yaml")
RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")
ITERATIONS_FILE = Path("state/ITERATIONS.md")
RESEARCH_SUMMARY_FILE = Path("state/RESEARCH_SUMMARY.md")


@dataclass
class Task:
    task_id: str
    stage: str
    status: str
    depends_on: List[str]
    assignee: Optional[str] = None
    command: Optional[str] = None


def load_manifest() -> dict:
    if not MANIFEST.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST}")
    with MANIFEST.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def ready_tasks(manifest: dict, branch: str) -> List[Task]:
    branches = manifest.get("branches", {})
    if branch not in branches:
        raise ValueError(f"Branch '{branch}' not defined in manifest")
    tasks = []
    for item in branches[branch].get("tasks", []):
        deps = item.get("depends_on", []) or []
        if item.get("status") in {"todo", "needs_rerun"} and all(
            dep_completed(branches[branch]["tasks"], dep) for dep in deps
        ):
            tasks.append(
                Task(
                    task_id=item["id"],
                    stage=item.get("stage", ""),
                    status=item.get("status", ""),
                    depends_on=deps,
                    assignee=item.get("assignee"),
                    command=item.get("command"),
                )
            )
    return tasks


def dep_completed(task_list: List[dict], dep_id: str) -> bool:
    for task in task_list:
        if task.get("id") == dep_id:
            return task.get("status") == "done"
    return False


def validate_artifacts() -> None:
    """Enforce naming and registration conventions before launching tasks."""
    errors: List[str] = []

    if RESULTS_DIR.exists():
        allowed_prefixes = (
            "style_",
            "fact_",
            "outline_",
            "draft_",
            "question_",
            "readability_",
            "package_",
            "post_",
            "assets_",
            "report_",
            "README",
        )
        style_reports = []
        fact_logs = []
        for path in sorted(RESULTS_DIR.glob("*")):
            if path.is_dir():
                continue
            if path.name.startswith('.'):
                continue
            if path.name.startswith(allowed_prefixes):
                if path.name.startswith("style_"):
                    style_reports.append(path.name)
                if path.name.startswith("fact_"):
                    fact_logs.append(path.name)
                continue
            errors.append(
                "results/{name} 命名不符合约定（需以 style_/fact_/outline_/draft_/question_/readability_/package_/post_/assets_/report_ 开头）。".format(
                    name=path.name
                )
            )

        if style_reports and ITERATIONS_FILE.exists():
            iterations_text = ITERATIONS_FILE.read_text(encoding="utf-8")
            missing_styles = [name for name in style_reports if name not in iterations_text]
            if missing_styles:
                errors.append(
                    "以下风格报告未登记在 state/ITERATIONS.md: " + ", ".join(missing_styles)
                )
        if fact_logs and RESEARCH_SUMMARY_FILE.exists():
            summary_text = RESEARCH_SUMMARY_FILE.read_text(encoding="utf-8")
            iterations_text = (
                ITERATIONS_FILE.read_text(encoding="utf-8")
                if ITERATIONS_FILE.exists()
                else ""
            )
            missing_facts = [
                name
                for name in fact_logs
                if name not in summary_text and name not in iterations_text
            ]
            if missing_facts:
                errors.append(
                    "以下事实核查日志未在 state/RESEARCH_SUMMARY.md 或 state/ITERATIONS.md 中引用: "
                    + ", ".join(missing_facts)
                )

    if FIGURES_DIR.exists():
        for png in FIGURES_DIR.glob("*.png"):
            meta = png.with_suffix(".meta.json")
            if not meta.exists():
                errors.append(f"缺少图表元数据文件: figures/{meta.name}")
                continue
            try:
                text = meta.read_text(encoding="utf-8")
                data = json.loads(text)
            except (OSError, json.JSONDecodeError) as exc:  # pragma: no cover - best effort
                errors.append(f"无法解析 {meta}: {exc}")
                continue
            required_keys = {"paragraph", "description", "source", "license"}
            missing_keys = sorted(required_keys - set(data.keys()))
            if missing_keys:
                errors.append(
                    f"figures/{meta.name} 缺少字段: {', '.join(missing_keys)}"
                )
            if data.get("paragraph") is None:
                errors.append(f"figures/{meta.name} 未指定关联段落编号。")

    if errors:
        for msg in errors:
            print(f"[guard] {msg}")
        raise SystemExit(1)


def launch(task: Task, dry_run: bool = True, async_mode: bool = False) -> None:
    print(f"[ready] {task.task_id} (stage={task.stage}, assignee={task.assignee})")
    if dry_run or not task.command:
        return
    shell_cmd = task.command
    if async_mode:
        subprocess.Popen(shell_cmd, shell=True, check=False)
    else:
        subprocess.run(shell_cmd, shell=True, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Trigger manifest tasks")
    parser.add_argument("--branch", default="main", help="Branch defined in manifest")
    parser.add_argument("--stage", help="Filter by stage name")
    parser.add_argument("--run", action="store_true", help="Execute associated command")
    parser.add_argument("--async", action="store_true", dest="async_mode", help="Run command without waiting")
    args = parser.parse_args()

    validate_artifacts()
    manifest = load_manifest()
    tasks = ready_tasks(manifest, args.branch)
    filtered = [t for t in tasks if not args.stage or t.stage == args.stage]

    if not filtered:
        print("No ready tasks found.")
        return

    for task in filtered:
        launch(task, dry_run=not args.run, async_mode=args.async_mode)


if __name__ == "__main__":
    main()
