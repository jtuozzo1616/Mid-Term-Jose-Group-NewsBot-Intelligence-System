"""Provenance-aware evaluations. No fabricated benchmark claims."""
from __future__ import annotations
from collections import Counter
from sklearn.model_selection import StratifiedKFold,cross_val_predict
from sklearn.metrics import classification_report,accuracy_score,f1_score,confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def evaluate_classification_cv(articles,folds:int=3)->dict:
    labeled=[a for a in articles if a.category]
    counts=Counter(a.category for a in labeled)
    if len(counts)<2 or min(counts.values())<folds:
        return {'status':'insufficient_data','reason':f'At least {folds} instances per class required'}
    model=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2))),
                    ('classifier',LogisticRegression(max_iter=1000,random_state=42))])
    gold=[a.category for a in labeled]
    pred=cross_val_predict(model,[a.full_text for a in labeled],gold,
          cv=StratifiedKFold(n_splits=folds,shuffle=True,random_state=42))
    return {'status':'ok','n_articles':len(labeled),'method':f'{folds}-fold stratified out-of-fold prediction',
            'accuracy':round(float(accuracy_score(gold,pred)),4),
            'macro_f1':round(float(f1_score(gold,pred,average='macro')),4),
            'per_class':classification_report(gold,pred,output_dict=True,zero_division=0),
            'classes':sorted(counts),'confusion_matrix':confusion_matrix(gold,pred,labels=sorted(counts)).tolist(),
            'limitation':'This evaluates the provided corpus only; synthetic fixture scores have no external validity'}


def evaluate_retrieval(engine,fixtures:list[tuple[str,str]],k:int=3)->dict:
    outcomes=[]
    for question,expected_id in fixtures:
        retrieved=[x['article_id'] for x in engine.search(question,k)]
        outcomes.append({'query':question,'expected':expected_id,'top_k':retrieved,
                        'reciprocal_rank':round(1/(retrieved.index(expected_id)+1),4) if expected_id in retrieved else 0.0})
    return {'queries':len(fixtures),'recall_at_k':round(sum(x['reciprocal_rank']>0 for x in outcomes)/max(len(outcomes),1),4),
            'mrr_at_k':round(sum(x['reciprocal_rank'] for x in outcomes)/max(len(outcomes),1),4),
            'retrieval_method':engine.retriever.method,
            'evaluation_type':'hand-authored synthetic retrieval probes','details':outcomes}
