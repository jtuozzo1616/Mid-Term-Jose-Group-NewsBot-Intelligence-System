"""Reproducible synthetic-data research extension. Do not misreport as BBC results.
Run: python run_research.py
"""
from __future__ import annotations
import json,time,platform,sys
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from newsbot2.io import import_articles
from newsbot2.engine import NewsBotEngine
from newsbot2.evaluation import evaluate_classification_cv,evaluate_retrieval
from newsbot2.language import pivot_terms

ROOT=Path(__file__).resolve().parent
ART=ROOT/'artifacts';ART.mkdir(exist_ok=True)
corpus=import_articles(ROOT/'data/demo_news.jsonl')
start=time.perf_counter();eng=NewsBotEngine(corpus)
build_sec=time.perf_counter()-start
# Hand-authored fictional queries target passages and known article identifiers;
# cannot be treated as an independent labeled newsroom benchmark.
probes=[
 ('chip artificial intelligence energy','demo-tech-1'),
 ('robot cameras sensors navigation','demo-tech-2'),
 ('bank loan review','demo-business-3'),
 ('shipping logistics delays','demo-business-4'),
 ('election polling accessibility proposal','demo-politics-2'),
 ('school budget public hearings','demo-politics-5'),
 ('cycling route signs safety','demo-sport-5'),
 ('swimming championship roster','demo-sport-4'),
 ('theatre drama production','demo-entertainment-3'),
 ('animation storytelling festival','demo-entertainment-5'),
 ('robótica navegación universidad','demo-tech-6'),
 ('empresa energía inversión mercado','demo-business-6'),
 ('gouvernement politique transport','demo-politics-6'),
 ('sport fußballturnier','demo-sport-6'),
 ('cinéma programme musique','demo-entertainment-6'),
 # Deliberate cross-language concept queries; these were manually crafted
 # after exploring vocabulary in the fictional records (no held-out claim).
 ('investigación datos privacidad','demo-tech-3'),
 ('deportes fútbol','demo-sport-1'),
 ('política elecciones','demo-politics-2'),
 ('cine música','demo-entertainment-6'),
 ('économie marché','demo-business-6'),
 ('forschung daten','demo-tech-3'),
 ('fußball sport','demo-sport-1'),
 ('technologie robotique','demo-tech-2'),
 ('regierung politik','demo-politics-6'),
]
pivoted=evaluate_retrieval(eng,probes,k=3)
# Ablation: same TF-IDF hyperparameters, but no multilingual pivot lexicon.
vectorizer=TfidfVectorizer(ngram_range=(1,2),stop_words='english',
                          sublinear_tf=True,strip_accents='unicode')
vectors=vectorizer.fit_transform([a.full_text.lower() for a in corpus])
naive=[]
for query,expected in probes:
    scores=cosine_similarity(vectorizer.transform([query.lower()]),vectors).ravel()
    ids=[corpus[i].article_id for i in scores.argsort()[::-1][:3] if scores[i]>0]
    rr=round(1/(ids.index(expected)+1),4) if expected in ids else 0
    naive.append({'query':query,'expected':expected,'top_k':ids,'reciprocal_rank':rr})
naive_mrr=sum(row['reciprocal_rank'] for row in naive)/len(naive)
naive_recall=sum(row['reciprocal_rank']>0 for row in naive)/len(naive)
cv=evaluate_classification_cv(corpus,folds=3)
# Condition not validated with external sources: all 30 are authored examples.
manifest={'experiment':'NewsBot 2.0 — transparently synthetic controlled probe',
  'date_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
  'python':sys.version.split()[0],'platform':platform.platform(),
  'source':'data/demo_news.jsonl','source_type':'hand-authored fictional articles',
  'n_records':len(corpus),'n_languages':len({a.language for a in corpus}),
  'n_topics':len({a.category for a in corpus}),
  'all_examples_synthetic':all(a.synthetic for a in corpus),
  'sha256_manifest':[{'article_id':a.article_id,'sha256':a.sha256} for a in corpus],
  'retriever_build_seconds':round(build_sec,5),
  'retrieval_probes':{'n':len(probes),'k':3,
      'pivot_mrr':pivoted['mrr_at_k'],'pivot_recall_at_k':pivoted['recall_at_k'],
      'naive_mrr':round(naive_mrr,4),'naive_recall_at_k':round(naive_recall,4),
      'interpretation':'In-corpus hand-authored probes, some selected after inspecting results; not independent cross-language validation',
      'pivot_examples':pivoted['details'],'ablation_no_pivot_examples':naive},
  'synthetic_classification_cv':cv,
  'limitations':['No independent newsroom or multilingual benchmark',
                 'No generative LLM evaluation',
                 'No installed offline translation pack in the default environment',
                 'The midterm BBC scores must not be substituted for these synthetic results']}
(ART/'research_results.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
(ART/'demo_cv.json').write_text(json.dumps(cv,indent=2),encoding='utf-8')
print('Saved artifacts/research_results.json')
print('Retrieval MRR@3 pivot / no pivot:',pivoted['mrr_at_k'],round(naive_mrr,4))
print('Synthetic classification CV macro-F1:',cv['macro_f1'])
