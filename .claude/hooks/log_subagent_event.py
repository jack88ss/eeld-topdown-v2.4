#!/usr/bin/env python3
import sys, json, os, datetime

def append_log(project_dir, actor, stage, change, evidence):
    log_path = os.path.join(project_dir, "state", "LOG.md")
    # Ensure header
    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("| time (UTC) | actor | stage | change | evidence |\n")
            f.write("|------------|-------|-------|--------|----------|\n")
    # Append row
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    row = f"| {now} | {actor} | {stage} | {change} | {evidence} |\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(row)

def main():
    data = json.load(sys.stdin)
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    tool = data.get("tool_name", "")
    if tool != "Task":
        return  # only log subagent runs here
    ti = data.get("tool_input", {}) or {}
    tr = data.get("tool_response", {}) or {}
    # Best-effort extraction
    actor = ti.get("name") or ti.get("agent") or ti.get("subagent") or ti.get("task") or "subagent"
    stage = ti.get("description") or ti.get("goal") or ti.get("task") or "task"
    # Keep evidence small: point to transcript path and any obvious status
    transcript = data.get("transcript_path", "")
    status = tr.get("status") or tr.get("result") or "ok"
    evidence = (transcript or "").split("/")[-1]
    change = f"Task completed: status={status}"
    append_log(project_dir, actor, stage, change, evidence)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Non-blocking: write to stderr so Claude shows it if needed
        sys.stderr.write(f"[log_subagent_event] {e}\n")
        sys.exit(1)
