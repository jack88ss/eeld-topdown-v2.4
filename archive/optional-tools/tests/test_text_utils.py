from pathlib import Path

from src.blog_pipeline.text_utils import analyse_text, split_paragraphs, split_sentences


def test_split_paragraphs_and_sentences():
    text = "你好啊？我今天测试。\n\n你觉得这样可以吗？当然可以！"
    paragraphs = split_paragraphs(text)
    assert len(paragraphs) == 2
    sentences = split_sentences(paragraphs[0])
    assert sentences == ["你好啊？", "我今天测试。"]


def test_analyse_text_basic_counts(tmp_path: Path):
    text = "你会喜欢这种方式吗？我觉得你会喜欢。\n\n我们继续探索吧。"
    metrics = analyse_text(text)
    assert metrics.total_sentences == 3
    assert metrics.question_sentences == 1
    assert metrics.second_person_count >= 2
    assert metrics.figure_mentions == 0
