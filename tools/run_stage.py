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
FIGURES_DIR = Path("figures")
ASSETS_DIR = Path("assets")


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
    """Friendly checks before运行任务."""
    issues: List[str] = []

    if not MANIFEST.exists():
        issues.append("缺少 state/STATUS.yaml，无法解析任务图。")

    if FIGURES_DIR.exists():
        metas = sorted(FIGURES_DIR.glob("*.meta.json"))
        for meta in metas:
            try:
                data = json.loads(meta.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                issues.append(f"无法解析 {meta.name}: {exc}")
                continue
            for key in ("paragraph", "description", "source", "license"):
                if not data.get(key):
                    issues.append(f"{meta.name} 缺少字段 {key}")
        # 发现有图片却无 meta
        pngs = {p.name for p in FIGURES_DIR.glob("*.png")}
        meta_pngs = {meta.with_suffix(".png").name for meta in metas}
        missing_meta = pngs - meta_pngs
        if missing_meta:
            issues.append("以下图片缺少 .meta.json: " + ", ".join(sorted(missing_meta)))

    if ASSETS_DIR.exists() and FIGURES_DIR.exists():
        asset_files = {p.name for p in ASSETS_DIR.glob("*.png")}
        referenced = {meta.with_suffix(".png").name for meta in FIGURES_DIR.glob("*.meta.json")}
        missing_assets = referenced - asset_files
        if missing_assets:
            issues.append("figures 中记录的图片在 assets/ 中不存在: " + ", ".join(sorted(missing_assets)))

    if issues:
        for msg in issues:
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
