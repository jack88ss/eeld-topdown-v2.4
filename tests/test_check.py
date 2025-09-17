from pathlib import Path

from src.blog_pipeline.check import check_draft, fact_check, load_profile
from src.blog_pipeline.style import extract_profile, write_style_profile

SAMPLE_TEXT = """
你是不是也会突然冒出灵感？我会立刻记下来，哪怕只有十几个字。\n\n这就像给未来的自己种一颗提醒的种子。![[assets/example.png]]
""".strip()


def prepare_profile(tmp_path: Path) -> Path:
    corpus_file = tmp_path / "corpus.txt"
    corpus_file.write_text(SAMPLE_TEXT, encoding="utf-8")
    profile = extract_profile([corpus_file])
    output = tmp_path / "STYLE_PROFILE.md"
    write_style_profile(profile, output, [corpus_file])
    return output


def test_check_draft_pass(tmp_path: Path):
    profile_path = prepare_profile(tmp_path)
    draft = tmp_path / "post.md"
    draft.write_text(
        SAMPLE_TEXT + "\n\n根据官方文档我又整理了一份步骤[@keyDoc]。",
        encoding="utf-8",
    )
    sources = tmp_path / "SOURCES.md"
    sources.write_text("- [keyDoc] 官方文档 — 内容；2024-01-01；链接：https://example.com\n", encoding="utf-8")

    report = check_draft(draft, profile_path)
    assert report.passed
    log_text, missing = fact_check(draft, sources)
    assert "[@keyDoc]" in log_text
    assert not missing


def test_check_draft_failures(tmp_path: Path):
    profile_path = prepare_profile(tmp_path)
    low_question_draft = tmp_path / "post_low.md"
    low_question_draft.write_text("这是一个没有问号的句子。\n\n也没有第二人称。", encoding="utf-8")
    report = check_draft(low_question_draft, profile_path)
    assert not report.passed
    assert report.style_match_score < 0.85
