"""Command line interface for the blog-writing pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .check import check_draft, fact_check, save_fact_log, save_style_report
from .style import extract_profile, write_style_profile


DEFAULT_STYLE_OUTPUT = Path("state/STYLE_PROFILE.md")
DEFAULT_STYLE_REPORT = Path("results/style_check.json")
DEFAULT_FACT_LOG = Path("results/fact_check.log")
DEFAULT_SOURCES = Path("state/SOURCES.md")


def _collect_files(path: Path, pattern: str) -> Sequence[Path]:
    if path.is_file():
        return [path]
    if not path.exists():
        raise FileNotFoundError(f"Corpus path not found: {path}")
    files = sorted(p for p in path.glob(pattern) if p.is_file())
    if not files:
        raise FileNotFoundError(f"No files matched pattern '{pattern}' under {path}")
    return files


def cmd_init_style(args: argparse.Namespace) -> None:
    corpus_root = Path(args.corpus)
    files = _collect_files(corpus_root, args.glob)
    profile = extract_profile(files)
    output_path = Path(args.output) if args.output else DEFAULT_STYLE_OUTPUT
    write_style_profile(profile, output_path, files)
    print(f"✅ 风格画像已写入 {output_path}（共 {profile.total_documents} 篇样例）")


def cmd_check(args: argparse.Namespace) -> None:
    draft_path = Path(args.draft)
    profile_path = Path(args.profile) if args.profile else DEFAULT_STYLE_OUTPUT
    sources_path = Path(args.sources) if args.sources else DEFAULT_SOURCES
    style_report_path = Path(args.style_output) if args.style_output else DEFAULT_STYLE_REPORT
    fact_log_path = Path(args.fact_output) if args.fact_output else DEFAULT_FACT_LOG

    report = check_draft(draft_path, profile_path)
    save_style_report(report, style_report_path)

    log_text, missing_keys = fact_check(draft_path, sources_path)
    save_fact_log(log_text, fact_log_path)

    status = "通过" if report.passed and not missing_keys else "需改进"
    print(f"✅ 风格检查输出 {style_report_path}")
    print(f"✅ 事实校验输出 {fact_log_path}")
    print(f"风格匹配分：{report.style_match_score:.3f} —— {status}")
    if report.messages:
        for msg in report.messages:
            print(f"⚠️ {msg}")
    if missing_keys:
        print("⚠️ 缺失引用键：" + ", ".join(missing_keys))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Blog writing pipeline helper")
    sub = parser.add_subparsers(dest="command")

    p_style = sub.add_parser("init-style", help="Analyse sample articles and build STYLE_PROFILE.md")
    p_style.add_argument("--corpus", default="/Users/wsy/Dropbox/example-blog-articles/", help="样例文章目录或文件路径")
    p_style.add_argument("--glob", default="*.txt", help="文件匹配模式")
    p_style.add_argument("--output", help="输出文件路径，默认 state/STYLE_PROFILE.md")
    p_style.set_defaults(func=cmd_init_style)

    p_check = sub.add_parser("check", help="Run style + fact checks on a draft")
    p_check.add_argument("--draft", default="draft/post.md", help="Markdown 草稿路径")
    p_check.add_argument("--profile", help="STYLE_PROFILE.md 路径")
    p_check.add_argument("--sources", help="state/SOURCES.md 路径")
    p_check.add_argument("--style-output", help="风格检查结果输出路径")
    p_check.add_argument("--fact-output", help="事实校验日志输出路径")
    p_check.set_defaults(func=cmd_check)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
