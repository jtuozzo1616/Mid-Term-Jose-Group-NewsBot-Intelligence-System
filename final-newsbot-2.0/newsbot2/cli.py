"""Scriptable local entry point: python -m newsbot2.cli ..."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import import_articles
from .engine import NewsBotEngine
from .analysis import Classifier

def main():
    p=argparse.ArgumentParser(description='NewsBot 2.0 | evidence-first local NLP')
    p.add_argument('command',choices=['overview','analyze','search','ask','topics','evaluate','train','translate'])
    p.add_argument('--corpus',default='data/demo_news.jsonl')
    p.add_argument('--id',default='demo-tech-1')
    p.add_argument('--query',default='artificial intelligence research')
    p.add_argument('--source-language',default='es')
    p.add_argument('--target-language',default='en')
    p.add_argument('--model',default='',help='Trusted locally built midterm joblib (never untrusted pickle)')
    p.add_argument('--multilingual-model',default='',help='Opt-in SentenceTransformers model; download may be necessary')
    p.add_argument('--retrieval-mode',choices=['tfidf','lsa'],default='tfidf')
    a=p.parse_args()
    classifier=Classifier.from_trusted_joblib(a.model) if a.model else Classifier()
    eng=NewsBotEngine(import_articles(a.corpus),classifier,
                      embedding_model=a.multilingual_model or None,retrieval_mode=a.retrieval_mode)
    if a.command=='overview':result=eng.overview()
    elif a.command=='analyze':result=eng.analyze(a.id)
    elif a.command=='search':result=eng.search(a.query)
    elif a.command=='ask':result=eng.ask(a.query)
    elif a.command=='topics':result=eng.topics()
    elif a.command=='evaluate':
        from .evaluation import evaluate_classification_cv
        result=evaluate_classification_cv(eng.articles)
    elif a.command=='train':result=eng.train_local_classifier()
    else:result=eng.translate(a.query,a.source_language,a.target_language)
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
