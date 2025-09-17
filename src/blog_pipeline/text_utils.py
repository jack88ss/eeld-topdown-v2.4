"""Helper routines for analysing Chinese/Markdown blog text."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, List

_PUNCTUATION = "。！？!?…；;"
_SECOND_PERSON_TOKENS = ("你", "你们", "您的", "妳", "妳们")


@dataclass
class TextMetrics:
    sentence_lengths: List[int]
    paragraph_lengths: List[int]
    question_sentences: int
    total_sentences: int
    second_person_count: int
    figure_mentions: int
    total_chars: int

    @property
    def avg_sentence_length(self) -> float:
        if not self.sentence_lengths:
            return 0.0
        return sum(self.sentence_lengths) / len(self.sentence_lengths)

    @property
    def avg_paragraph_length(self) -> float:
        if not self.paragraph_lengths:
            return 0.0
        return sum(self.paragraph_lengths) / len(self.paragraph_lengths)

    @property
    def question_ratio(self) -> float:
        if self.total_sentences == 0:
            return 0.0
        return self.question_sentences / self.total_sentences

    @property
    def second_person_ratio(self) -> float:
        if self.total_chars == 0:
            return 0.0
        return self.second_person_count / self.total_chars


def split_paragraphs(text: str) -> List[str]:
    """Return list of paragraphs, ignoring empty lines."""
    raw = re.split(r"\n\s*\n", text.strip())
    paragraphs = [p.strip() for p in raw if p.strip()]
    return paragraphs


def split_sentences(paragraph: str) -> List[str]:
    """Split a paragraph into sentences while keeping Chinese punctuation."""
    if not paragraph.strip():
        return []
    parts: List[str] = []
    buffer = []
    for char in paragraph:
        buffer.append(char)
        if char in _PUNCTUATION:
            parts.append("".join(buffer).strip())
            buffer = []
    if buffer:
        remainder = "".join(buffer).strip()
        if remainder:
            parts.append(remainder)
    return [p for p in parts if p]


def analyse_text(text: str) -> TextMetrics:
    """Compute basic metrics for the given markdown text."""
    paragraphs = split_paragraphs(text)
    sentence_lengths: List[int] = []
    paragraph_lengths: List[int] = []
    question_sentences = 0
    total_sentences = 0
    second_person_count = 0
    figure_mentions = len(re.findall(r"!\[\[", text))

    cleaned_text = re.sub(r"\s", "", text)
    total_chars = len(cleaned_text)
    for token in _SECOND_PERSON_TOKENS:
        second_person_count += cleaned_text.count(token)

    for paragraph in paragraphs:
        sentences = split_sentences(paragraph)
        total_sentences += len(sentences)
        paragraph_len = len(re.sub(r"\s", "", paragraph))
        if paragraph_len:
            paragraph_lengths.append(paragraph_len)
        for sentence in sentences:
            sentence_len = len(re.sub(r"\s", "", sentence))
            if sentence_len:
                sentence_lengths.append(sentence_len)
            if "?" in sentence or "？" in sentence:
                question_sentences += 1

    return TextMetrics(
        sentence_lengths=sentence_lengths,
        paragraph_lengths=paragraph_lengths,
        question_sentences=question_sentences,
        total_sentences=total_sentences,
        second_person_count=second_person_count,
        figure_mentions=figure_mentions,
        total_chars=total_chars,
    )


def top_keywords(texts: Iterable[str], top_n: int = 10) -> List[str]:
    """Extract naive top keywords by frequency (Chinese bigrams + short words)."""
    freq: dict[str, int] = {}
    for text in texts:
        cleaned = re.sub(r"[^\w\u4e00-\u9fa5]", " ", text)
        for token in cleaned.split():
            if len(token) == 1:
                continue
            freq[token] = freq.get(token, 0) + 1
        chars = re.sub(r"\s", "", text)
        for i in range(len(chars) - 1):
            bigram = chars[i : i + 2]
            if any(ch.isdigit() for ch in bigram):
                continue
            freq[bigram] = freq.get(bigram, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:top_n]]
