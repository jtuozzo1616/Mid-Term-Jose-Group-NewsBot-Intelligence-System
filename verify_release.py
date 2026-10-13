#!/usr/bin/env python3
"""Check release artifacts after *real* BBC corpus execution; never make up scores."""
import argparse, hashlib, json, sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
REQUIRED=['01_data_distribution.png','02_tfidf_category_terms.png','03_linguistic_sentiment.png',
'04_ner_analysis.png','05_model_cv_comparison.png','06_confusion_matrix.png','07_entity_comentions.png','08_robustness_stress_test.png',
'feature_ablation.csv','robustness_stress_test.csv','bootstrap_uncertainty.json','model_cv_comparison.csv','per_class_metrics.csv','error_analysis_excerpt.csv','classification_report.txt',
'holdout_metrics.json','insights.json','run_manifest.json','newsbot_classifier.joblib','EVIDENCE_BASED_FINDINGS.txt']
def verify(out):
    missing=[f for f in REQUIRED if not (out/f).is_file() or (out/f).stat().st_size==0]
    if missing:raise AssertionError('Missing/empty real run outputs: '+', '.join(missing))
    r=json.loads((out/'run_manifest.json').read_text(encoding='utf-8'))
    i=json.loads((out/'insights.json').read_text(encoding='utf-8'))
    m=pd.read_csv(out/'per_class_metrics.csv')
    c=pd.read_csv(out/'model_cv_comparison.csv')
    assert r.get('notebook_execution_status')=='REAL_DATA_EXECUTED', 'Real-data run not attested by notebook'
    assert r.get('dataset_origin') in {'user_supplied_Kaggle_CSV','public_research_mirror_of_Kaggle_competition_CSV'},'Unknown source'
    assert len(r.get('source_file_sha256',''))==64, 'Missing dataset hash'
    assert 500 <= r['rows'] <= 2000, 'BBC article count out of assignment range'
    assert r['train_rows']+r['holdout_rows']==r['rows'],'Invalid split sizes'
    assert len(m)==5 and len(c)>=4,'Expected five labels and four model families'
    assert set(m.category)=={'business','entertainment','politics','sport','tech'},'Incorrect labels'
    assert len(i['dataset']['labels'])==5,'Wrong dataset category count'
    assert 0<=float(r['holdout_macro_f1'])<=1 and 0<=float(r['holdout_accuracy'])<=1
    assert not m[['precision','recall','f1']].isna().any().any(), 'Undefined metrics'
    print('PASS: genuine 5-class NewsBot run: %d documents, %.4f macro-F1, %.4f accuracy, %s' %
        (r['rows'],r['holdout_macro_f1'],r['holdout_accuracy'],r['selected_model']))
    return r
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--outputs',default='outputs');a=parser.parse_args()
    try:verify(ROOT/a.outputs)
    except Exception as e:print('INCOMPLETE:',e);sys.exit(1)
