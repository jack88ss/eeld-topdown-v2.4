from pathlib import Path

from src.blog_pipeline.style import extract_profile, write_style_profile


SAMPLE_TEXT = """
你是不是也有这种烦恼？我总在关键时刻想起一个点子，却没有来得及记录。

后来我学会了随手打开手机，对着空气说出一句话。这就像给未来的自己留下路标。

![[assets/example.png]]

你可以挑一个你最顺手的工具，别纠结格式，先把想法留住。
""".strip()


def test_extract_profile(tmp_path: Path):
    corpus_dir = tmp_path / "corpus"
    corpus_dir.mkdir()
    (corpus_dir / "a.txt").write_text(SAMPLE_TEXT, encoding="utf-8")
    (corpus_dir / "b.txt").write_text(SAMPLE_TEXT.replace("烦恼", "困扰"), encoding="utf-8")

    profile = extract_profile(list(corpus_dir.glob("*.txt")))
    assert profile.total_documents == 2
    assert profile.avg_sentence_length > 0
    assert profile.min_question_ratio >= 0.03
    assert profile.min_second_person_count >= 8

    output = tmp_path / "STYLE_PROFILE.md"
    write_style_profile(profile, output, list(corpus_dir.glob("*.txt")))
    text = output.read_text(encoding="utf-8")
    assert "风格画像" in text
    cache = output.with_suffix(".json")
    assert cache.exists()
