"""Optional helper to aggregate style metrics; default workflow relies on agents."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from statistics import mean
from typing import Iterable, List, Sequence

from .text_utils import TextMetrics, analyse_text, split_paragraphs, top_keywords

SECOND_PERSON_TOKENS = ("你", "你们", "您的", "妳", "妳们")


@dataclass
class StyleProfile:
    avg_sentence_length: float
    max_sentence_length: float
    avg_paragraph_length: float
    question_ratio: float
    min_question_ratio: float
    second_person_ratio: float
    min_second_person_count: int
    figure_density: float
    avg_figures_per_article: float
    keywords: List[str]
    representative_paragraphs: List[str]
    total_documents: int

    def to_dict(self) -> dict:
        return {
            "avg_sentence_length": round(self.avg_sentence_length, 2),
            "max_sentence_length": round(self.max_sentence_length, 2),
            "avg_paragraph_length": round(self.avg_paragraph_length, 2),
            "question_ratio": round(self.question_ratio, 4),
            "min_question_ratio": round(self.min_question_ratio, 4),
            "second_person_ratio": round(self.second_person_ratio, 4),
            "min_second_person_count": int(self.min_second_person_count),
            "figure_density": round(self.figure_density, 4),
            "avg_figures_per_article": round(self.avg_figures_per_article, 2),
            "keywords": self.keywords,
            "representative_paragraphs": self.representative_paragraphs,
            "total_documents": self.total_documents,
            "second_person_tokens": list(SECOND_PERSON_TOKENS),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StyleProfile":
        return cls(
            avg_sentence_length=data["avg_sentence_length"],
            max_sentence_length=data["max_sentence_length"],
            avg_paragraph_length=data["avg_paragraph_length"],
            question_ratio=data["question_ratio"],
            min_question_ratio=data["min_question_ratio"],
            second_person_ratio=data["second_person_ratio"],
            min_second_person_count=data["min_second_person_count"],
            figure_density=data["figure_density"],
            avg_figures_per_article=data.get("avg_figures_per_article", 0.0),
            keywords=data.get("keywords", []),
            representative_paragraphs=data.get("representative_paragraphs", []),
            total_documents=data.get("total_documents", 0),
        )


@dataclass
class CorpusStats:
    metrics: List[TextMetrics]
    paragraphs: List[str]
    total_figures: int
    total_documents: int


def _collect_corpus_stats(paths: Sequence[Path]) -> CorpusStats:
    metrics: List[TextMetrics] = []
    paragraphs: List[str] = []
    total_figures = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        tm = analyse_text(text)
        metrics.append(tm)
        total_figures += tm.figure_mentions
        paragraphs.extend(split_paragraphs(text))
    return CorpusStats(
        metrics=metrics,
        paragraphs=[p for p in paragraphs if len(p.strip()) >= 20],
        total_figures=total_figures,
        total_documents=len(paths),
    )


def _aggregate_metrics(stats: CorpusStats) -> StyleProfile:
    if not stats.metrics:
        raise ValueError("No documents found for style extraction")

    sentence_lengths: List[int] = []
    paragraph_lengths: List[int] = []
    total_question_sentences = 0
    total_sentences = 0
    total_second_person = 0
    total_chars = 0

    for metric in stats.metrics:
        sentence_lengths.extend(metric.sentence_lengths)
        paragraph_lengths.extend(metric.paragraph_lengths)
        total_question_sentences += metric.question_sentences
        total_sentences += metric.total_sentences
        total_second_person += metric.second_person_count
        total_chars += metric.total_chars

    avg_sentence_length = mean(sentence_lengths) if sentence_lengths else 0.0
    avg_paragraph_length = mean(paragraph_lengths) if paragraph_lengths else 0.0
    question_ratio = (
        total_question_sentences / total_sentences if total_sentences else 0.0
    )
    second_person_ratio = total_second_person / total_chars if total_chars else 0.0
    figure_density = (
        stats.total_figures / len(paragraph_lengths) if paragraph_lengths else 0.0
    )
    avg_figures_per_article = (
        stats.total_figures / stats.total_documents if stats.total_documents else 0.0
    )

    min_question_ratio = max(0.03, question_ratio * 0.8 if question_ratio else 0.03)
    max_sentence_length = max(24.0, avg_sentence_length * 1.1 if avg_sentence_length else 24.0)
    min_second_person_count = max(8, int(total_second_person / max(stats.total_documents, 1) * 0.7))

    keywords = top_keywords([p for p in stats.paragraphs], top_n=12)
    representative = _select_representative_paragraphs(stats.paragraphs)

    return StyleProfile(
        avg_sentence_length=avg_sentence_length,
        max_sentence_length=max_sentence_length,
        avg_paragraph_length=avg_paragraph_length,
        question_ratio=question_ratio,
        min_question_ratio=min_question_ratio,
        second_person_ratio=second_person_ratio,
        min_second_person_count=min_second_person_count,
        figure_density=figure_density,
        avg_figures_per_article=avg_figures_per_article,
        keywords=representative["keywords"],
        representative_paragraphs=representative["paragraphs"],
        total_documents=stats.total_documents,
    )


def _select_representative_paragraphs(paragraphs: Iterable[str]) -> dict:
    selected: List[str] = []
    by_question = [p for p in paragraphs if "？" in p or "?" in p]
    by_second_person = [p for p in paragraphs if any(token in p for token in SECOND_PERSON_TOKENS)]

    for group in (by_question, by_second_person, paragraphs):
        for paragraph in group:
            clean = paragraph.strip()
            if len(clean) < 30:
                continue
            if clean not in selected:
                selected.append(clean)
            if len(selected) >= 2:
                break
        if len(selected) >= 2:
            break

    keywords = top_keywords(selected if selected else paragraphs, top_n=10)
    return {"paragraphs": selected[:2], "keywords": keywords[:10]}


def extract_profile(corpus_paths: Sequence[Path]) -> StyleProfile:
    stats = _collect_corpus_stats(corpus_paths)
    return _aggregate_metrics(stats)


def write_style_profile(profile: StyleProfile, output_path: Path, corpus_paths: Sequence[Path]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    corpus_list = "\n".join(f"- {path}" for path in corpus_paths)
    paragraph_block = "\n\n".join(f"> {para.strip()}" for para in profile.representative_paragraphs) or "（示例文本不足，待补充）"
    keywords_line = ", ".join(profile.keywords[:10]) or "N/A"
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    profile_summary = profile.to_dict()
    front_matter_lines = ["profile:"]
    for key, value in profile_summary.items():
        if isinstance(value, list):
            joined = ", ".join(map(str, value))
            front_matter_lines.append(f"  {key}: {joined}")
        else:
            front_matter_lines.append(f"  {key}: {value}")
    front_matter_lines.append(f"  cached_at: {timestamp}")
    front_matter = "\n".join(front_matter_lines)

    body = f"""---
{front_matter}
---
# 风格画像

> 缓存自示例文章：
{corpus_list}

## 语气概览
- 平均句长：{profile.avg_sentence_length:.1f} 字（上限 {profile.max_sentence_length:.1f} 字）
- 平均段落长度：{profile.avg_paragraph_length:.1f} 字
- 问句占比：{profile.question_ratio*100:.1f}%（最低 {profile.min_question_ratio*100:.1f}%）
- 第二人称占比：{profile.second_person_ratio*100:.2f}%（每篇至少 {profile.min_second_person_count} 次）
- 平均配图：每篇 {profile.avg_figures_per_article:.1f} 张，段落配图密度 {profile.figure_density*100:.1f}%

## 关键词与表达
- 高频表达：{keywords_line}
- 常用二人称词：{', '.join(SECOND_PERSON_TOKENS)}

## 代表段落
{paragraph_block}

## 阈值建议
| 指标 | 目标 | 阈值 |
|------|------|------|
| 平均句长 | {profile.avg_sentence_length:.1f} 字 | ≤ {profile.max_sentence_length:.1f} 字 |
| 问句占比 | {profile.question_ratio*100:.1f}% | ≥ {profile.min_question_ratio*100:.1f}% |
| 第二人称次数 | 每篇 {profile.min_second_person_count+2} 次左右 | ≥ {profile.min_second_person_count} 次 |
| 配图密度 | {profile.figure_density*100:.1f}% | ≥ {profile.figure_density*100:.1f}% |

> 仅在替换新的示例文章时，才需要重新运行 `python -m src.blog_pipeline.cli init-style` 以刷新缓存。
"""
    output_path.write_text(body, encoding="utf-8")

    cache_path = output_path.with_suffix(".json")
    cache_payload = {
        "cached_at": timestamp,
        "corpus": [str(path) for path in corpus_paths],
        "profile": profile.to_dict(),
    }
    cache_path.write_text(json.dumps(cache_payload, ensure_ascii=False, indent=2), encoding="utf-8")
