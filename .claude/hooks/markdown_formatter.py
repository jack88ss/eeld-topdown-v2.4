#!/usr/bin/env python3
# Minimal markdown formatter: collapse >2 blank lines and ensure trailing newline.
import sys, json, os, re

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        # If stdin not JSON (unexpected), just exit quietly
        return
    tool = data.get("tool_name", "")
    if tool not in {"Write", "Edit", "MultiEdit"}:
        return
    path = (data.get("tool_input", {}) or {}).get("file_path", "")
    if not path or not path.endswith((".md", ".mdx")):
        return
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        formatted = re.sub(r"\n{3,}", "\n\n", content).rstrip() + "\n"
        if formatted != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"✓ formatted markdown: {path}")
    except Exception as e:
        sys.stderr.write(f"[markdown_formatter] {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
