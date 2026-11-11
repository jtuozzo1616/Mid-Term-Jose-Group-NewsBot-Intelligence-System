"""Validated import/export and fixtures; no uncontrolled network ingestion."""
from __future__ import annotations
from pathlib import Path
import csv,json
from .schemas import Article

MAX_ARTICLES=3000
MAX_FILE_BYTES=8_000_000


def import_articles(path: str|Path)->list[Article]:
    path=Path(path)
    if path.stat().st_size>MAX_FILE_BYTES:
        raise ValueError('Input exceeds 8 MB')
    if path.suffix.lower()=='.jsonl':
        with path.open(encoding='utf-8') as f:
            records=[json.loads(line) for line in f if line.strip()]
    elif path.suffix.lower()=='.csv':
        with path.open(encoding='utf-8-sig',newline='') as f:
            records=list(csv.DictReader(f))
    else:
        raise ValueError('Only .jsonl or .csv files supported')
    if len(records)>MAX_ARTICLES: raise ValueError('Corpus exceeds 3,000 articles')
    data=[];seen=set()
    for i,r in enumerate(records):
        if not isinstance(r,dict): raise ValueError('Every row must be an object')
        doc=Article(article_id=str(r.get('article_id') or f'user-{i+1:04d}'),
            title=r.get('title',''),body=r.get('body',''),source=r.get('source','User provided'),
            published_at=r.get('published_at',''),language=r.get('language') or 'auto',
            category=r.get('category') or '',url=r.get('url') or '',
            synthetic=str(r.get('synthetic','false')).lower()=='true' if isinstance(r.get('synthetic'),str) else bool(r.get('synthetic',False)))
        if doc.article_id in seen: raise ValueError(f'Duplicate id: {doc.article_id}')
        seen.add(doc.article_id);data.append(doc)
    return data


def export_jsonl(articles,path):
    with Path(path).open('w',encoding='utf-8') as f:
        for a in articles:f.write(json.dumps(a.to_dict(),ensure_ascii=False)+'\n')
