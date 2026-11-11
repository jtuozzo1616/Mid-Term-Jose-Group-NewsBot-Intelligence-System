"""Typed contract for articles and predictions. External text is never treated as instructions."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any
import hashlib
import re

MAX_TITLE = 240
MAX_BODY = 18_000


def normalize_text(value: str) -> str:
    """Whitespace/HTML cleanup with no remote fetch or script execution."""
    from html import unescape
    value = unescape(str(value or ''))
    value = re.sub(r'<[^>]*>', ' ', value)
    value = re.sub(r'[\u0000-\u001f\u007f]', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()


@dataclass(frozen=True)
class Article:
    article_id: str
    title: str
    body: str
    source: str = 'User provided'
    published_at: str = ''
    language: str = 'auto'
    category: str = ''
    url: str = ''
    synthetic: bool = False

    def __post_init__(self):
        if not re.fullmatch(r'[A-Za-z0-9._-]{1,80}', self.article_id):
            raise ValueError('article_id must contain 1–80 safe alphanumeric characters')
        object.__setattr__(self, 'title', normalize_text(self.title)[:MAX_TITLE])
        object.__setattr__(self, 'body', normalize_text(self.body)[:MAX_BODY])
        object.__setattr__(self, 'source', normalize_text(self.source)[:160])
        if not self.title or len(self.body) < 30:
            raise ValueError('An article needs a title and at least 30 characters of body text')
        if self.url and not self.url.startswith(('https://','http://')):
            raise ValueError('Only HTTP(S) source URLs are accepted')
        if self.language not in ('auto','en','es','fr','de'):
            raise ValueError('Unsupported language value')

    @property
    def full_text(self) -> str:
        return f'{self.title}. {self.body}'

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.full_text.encode('utf-8')).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SearchHit:
    article_id: str
    title: str
    score: float
    excerpt: str
    source: str
    synthetic: bool
    retrieval_method: str = 'tfidf'

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
