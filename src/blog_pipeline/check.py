"""Optional style/fact check scaffolding; manual编辑 remains primary."""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

from .style import StyleProfile
from .text_utils import TextMetrics, analyse_text, split_paragraphs


@dataclass
class StyleCheckReport:
    style_match_score: float
    avg_sentence_length: float
    avg_paragraph_length: float
    question_ratio: float
    second_person_ratio: float
    second_person_count: int
    figure_density: float
    figure_mentions: int
    question_sentences: int
    total_sentences: int
    messages: List[str]
    passed: bool

    def to_dict(self) -> dict:
        return {
            "style_match_score": round(self.style_match_score, 3),
            "avg_sentence_length": round(self.avg_sentence_length, 2),
            "avg_paragraph_length": round(self.avg_paragraph_length, 2),
            "question_ratio": round(self.question_ratio, 4),
            "second_person_ratio": round(self.second_person_ratio, 4),
            "second_person_count": self.second_person_count,
            "figure_density": round(self.figure_density, 4),
            "figure_mentions": self.figure_mentions,
            "question_sentences": self.question_sentences,
            "total_sentences": self.total_sentences,
            "messages": self.messages,
            "passed": self.passed,
        }


def load_profile(path: Path) -> StyleProfile:
    json_cache = path.with_suffix(".json")
    if json_cache.exists():
        payload = json.loads(json_cache.read_text(encoding="utf-8"))
        data = payload.get("profile", payload)
        return StyleProfile.from_dict(data)

    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if "profile:" in text:
        extracted: Dict[str, float] = {}
        for line in text.splitlines():
            if line.startswith("  ") and ":" in line:
                key, value = line.strip().split(":", 1)
                key = key.strip()
                value = value.strip()
                if not value:
                    continue
                if key in {"keywords", "representative_paragraphs", "second_person_tokens"}:
                    extracted[key] = [item.strip() for item in value.split(",") if item.strip()]
                else:
                    try:
                        extracted[key] = float(value)
                    except ValueError:
                        try:
                            extracted[key] = int(value)
                        except ValueError:
                            extracted[key] = value
        if extracted:
            return StyleProfile.from_dict(extracted)  # type: ignore[arg-type]
    raise FileNotFoundError(
        "Style profile cache 未找到，请运行 `python -m src.blog_pipeline.cli init-style` 生成缓存。"
    )


def _score(metric: float, target: float, mode: str) -> float:
    if target <= 0:
        return 1.0
    if mode == "max":
        if metric <= target:
            return 1.0
        diff = metric - target
        return max(0.0, 1 - diff / (target + 1e-6))
    if mode == "min":
        if metric >= target:
            return 1.0
        diff = target - metric
        return max(0.0, 1 - diff / (target + 1e-6))
    return 1.0


def _compute_style_score(metrics: TextMetrics, profile: StyleProfile) -> Tuple[float, List[str], Dict[str, float]]:
    p_data = profile.to_dict()
    avg_sentence_length = metrics.avg_sentence_length
    avg_paragraph_length = metrics.avg_paragraph_length
    question_ratio = metrics.question_ratio
    second_person_ratio = metrics.second_person_ratio
    second_person_count = metrics.second_person_count
    figure_density = metrics.figure_mentions / max(len(metrics.paragraph_lengths), 1)

    scores = []
    messages: List[str] = []

    scores.append(_score(avg_sentence_length, profile.max_sentence_length, "max"))
    if avg_sentence_length > profile.max_sentence_length:
        messages.append(
            f"平均句长 {avg_sentence_length:.1f} 字，高于上限 {profile.max_sentence_length:.1f} 字。"
        )

    scores.append(_score(question_ratio, profile.min_question_ratio, "min"))
    if question_ratio < profile.min_question_ratio:
        messages.append(
            f"问句占比 {question_ratio*100:.1f}%，低于阈值 {profile.min_question_ratio*100:.1f}%。"
        )

    scores.append(_score(second_person_count, profile.min_second_person_count, "min"))
    if second_person_count < profile.min_second_person_count:
        messages.append(
            f"第二人称出现 {second_person_count} 次，低于最低要求 {profile.min_second_person_count} 次。"
        )

    if profile.figure_density > 0:
        target_density = profile.figure_density
        scores.append(_score(figure_density, target_density, "min"))
        if figure_density < target_density:
            messages.append(
                f"配图密度 {figure_density*100:.1f}% 低于目标 {target_density*100:.1f}%。"
            )
    else:
        scores.append(1.0)

    style_match_score = sum(scores) / len(scores)

    metric_summary = {
        "avg_sentence_length": avg_sentence_length,
        "avg_paragraph_length": avg_paragraph_length,
        "question_ratio": question_ratio,
        "second_person_ratio": second_person_ratio,
        "second_person_count": second_person_count,
        "figure_density": figure_density,
    }
    return style_match_score, messages, metric_summary


def check_draft(draft_path: Path, profile_path: Path) -> StyleCheckReport:
    text = draft_path.read_text(encoding="utf-8")
    profile = load_profile(profile_path)
    metrics = analyse_text(text)

    style_match_score, messages, metric_summary = _compute_style_score(metrics, profile)

    passed = (
        style_match_score >= 0.85
        and metric_summary["avg_sentence_length"] <= profile.max_sentence_length
        and metric_summary["question_ratio"] >= profile.min_question_ratio
        and metric_summary["second_person_count"] >= profile.min_second_person_count
    )

    return StyleCheckReport(
        style_match_score=style_match_score,
        avg_sentence_length=metric_summary["avg_sentence_length"],
        avg_paragraph_length=metric_summary["avg_paragraph_length"],
        question_ratio=metric_summary["question_ratio"],
        second_person_ratio=metric_summary["second_person_ratio"],
        second_person_count=metric_summary["second_person_count"],
        figure_density=metric_summary["figure_density"],
        figure_mentions=metrics.figure_mentions,
        question_sentences=metrics.question_sentences,
        total_sentences=metrics.total_sentences,
        messages=messages,
        passed=passed,
    )


CITATION_PATTERN = re.compile(r"\[@([^\]]+)\]")
SOURCE_KEY_PATTERN = re.compile(r"- \[([^\]]+)\]")
URL_PATTERN = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")


def load_source_keys(path: Path) -> List[str]:
    if not path.exists():
        return []
    keys = SOURCE_KEY_PATTERN.findall(path.read_text(encoding="utf-8"))
    return keys


def fact_check(draft_path: Path, sources_path: Path) -> Tuple[str, List[str]]:
    text = draft_path.read_text(encoding="utf-8")
    paragraphs = split_paragraphs(text)
    keys_in_sources = set(load_source_keys(sources_path))
    citations = []
    missing_keys = set()

    for idx, paragraph in enumerate(paragraphs, start=1):
        for match in CITATION_PATTERN.finditer(paragraph):
            key = match.group(1)
            status = "OK" if key in keys_in_sources else "MISSING"
            if status == "MISSING":
                missing_keys.add(key)
            citations.append((idx, key, status))

    urls = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        for match in URL_PATTERN.finditer(paragraph):
            urls.append((idx, match.group(1)))

    lines = ["# Fact Check Report", f"Draft: {draft_path}"]
    lines.append(f"Total citations: {len(citations)}")
    lines.append(f"Missing citations: {len(missing_keys)}")
    lines.append("")
    lines.append("## Citations")
    for idx, key, status in citations:
        lines.append(f"P{idx}: [@{key}] — {status}")
    lines.append("")
    lines.append("## External URLs")
    if urls:
        for idx, url in urls:
            lines.append(f"P{idx}: {url}")
    else:
        lines.append("(none)")

    if missing_keys:
        lines.append("")
        lines.append("## Missing Keys")
        for key in sorted(missing_keys):
            lines.append(f"- {key}")

    return "\n".join(lines) + "\n", sorted(missing_keys)


def save_style_report(report: StyleCheckReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def save_fact_log(log_text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(log_text, encoding="utf-8")
