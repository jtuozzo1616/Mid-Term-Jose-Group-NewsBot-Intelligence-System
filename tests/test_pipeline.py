"""Offline regression checks. Uses generated synthetic documents ONLY; not BBC results."""
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
import os, unittest, json, html, re, time, hashlib, platform
from collections import Counter,defaultdict
from itertools import combinations
import nbformat
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
from sklearn.model_selection import train_test_split, StratifiedKFold,cross_validate, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report,ConfusionMatrixDisplay
from sklearn.base import clone
from scipy.special import softmax

NOTEBOOK=Path(__file__).parents[1]/'Midterm_NewsBot_Intelligence_System.ipynb'
NB=nbformat.read(NOTEBOOK,as_version=4)
@contextmanager
def cd(folder):
    before=os.getcwd()
    try:os.chdir(folder);yield
    finally:os.chdir(before)

VOC={
 'business':'stocks investors markets profits revenues finance earnings banking trade finance',
 'entertainment':'movie cinema films actors director music awards theaters dance singers',
 'politics':'election parliament legislation ministers senate voting campaign government law',
 'sport':'football tennis athletes tournament match striker coaches goal scoring race',
 'tech':'microchip processor artificial intelligence software robotics computers coding networks'
}
def fixture(n_per_class=105):
    rows=[]
    for j,(category,vocab) in enumerate(VOC.items()):
        for i in range(n_per_class):
            txt=((vocab+' reports analysts explain how events changed after the meeting. ')*7+
                 f' An illustrative article number {j*10000+i}, with example date 2024, closes the report.')
            rows.append({'ArticleId':j*10000+i,'Text':txt,'Category':category})
    return pd.DataFrame(rows)

def context(folder):
    return dict(DATA=Path(folder),OUT=Path(folder),Path=Path,np=np,pd=pd,plt=plt,sns=sns,
      re=re,html=html,os=os,spacy=spacy,nlp=spacy.blank('en'),SEED=42,
      Counter=Counter,defaultdict=defaultdict,combinations=combinations,
      time=time,hashlib=hashlib,platform=platform,train_test_split=train_test_split,
      StratifiedKFold=StratifiedKFold,cross_validate=cross_validate,GridSearchCV=GridSearchCV,
      TfidfVectorizer=TfidfVectorizer,Pipeline=Pipeline,MultinomialNB=MultinomialNB,
      LogisticRegression=LogisticRegression,LinearSVC=LinearSVC,DummyClassifier=DummyClassifier,
      accuracy_score=accuracy_score,f1_score=f1_score,classification_report=classification_report,
      ConfusionMatrixDisplay=ConfusionMatrixDisplay,clone=clone,softmax=softmax,display=lambda *x:None,
      json=json)

def run_cell(index,ns):exec(compile(NB.cells[index].source, f'<notebook-cell-{index}>','exec'),ns,ns)
class NewsBotTests(TestCase):
    def test_notebook_cells_parse(self):
        import ast
        for i,cell in enumerate(NB.cells):
            if cell.cell_type=='code' and not cell.source.startswith('%pip'):
                ast.parse(cell.source,filename=f'Cell_{i}')

    def test_loader_accepts_bbc_text_schema_and_deduplicates(self):
        with TemporaryDirectory() as d,cd(d):
            df=fixture();dup=df.iloc[[0]].copy();dup['ArticleId']=[55555]
            pd.concat([df,dup],ignore_index=True).to_csv('BBC News Train.csv',index=False)
            ctx=context(d);run_cell(5,ctx)
            self.assertEqual(len(ctx['df']),525)
            self.assertEqual(ctx['duplicates'],1)
            self.assertEqual(ctx['df'].category.nunique(),5)
            run_cell(8,ctx)
            self.assertEqual(len(ctx['df'].text_clean),525)
            self.assertIn('2025',ctx['normalize_text']('Not a good result in 2025!'))
            self.assertEqual(ctx['normalize_text'](None),'')

    def test_loader_accepts_article_schema(self):
        with TemporaryDirectory() as d,cd(d):
            fixture().rename(columns={'Text':'Article'}).to_csv('BBC News Train.csv',index=False)
            ctx=context(d);run_cell(5,ctx)
            self.assertEqual(len(ctx['df']),525)

    def test_loader_rejects_unlabeled_competition_test(self):
        with TemporaryDirectory() as d,cd(d):
            fixture().drop(columns=['Category']).to_csv('BBC News Train.csv',index=False)
            with self.assertRaises(ValueError):run_cell(5,context(d))

    def test_public_mirror_fallback_provenance_with_mock_download(self):
        # Mock the network using synthetic corpus bytes: no external dataset is claimed.
        from shutil import copyfile
        with TemporaryDirectory() as d,cd(d):
            source=Path(d)/'fixture_source.csv';fixture().to_csv(source,index=False)
            ctx=context(d)
            with patch('urllib.request.urlretrieve',side_effect=lambda url,destination:copyfile(source,destination)) as mocked:
                run_cell(5,ctx)
            self.assertEqual(ctx['DATA_ORIGIN'],'public_research_mirror_of_Kaggle_competition_CSV')
            self.assertEqual(len(ctx['df']),525)
            self.assertEqual(mocked.call_count,1)

    def test_quality_verifier_cannot_pass_without_real_artifacts(self):
        import sys
        sys.path.insert(0,str(NOTEBOOK.parent))
        from verify_release import verify
        with TemporaryDirectory() as d:
            with self.assertRaises(AssertionError):verify(Path(d))

    def test_robustness_extension_runs_on_synthetic_fixture(self):
        # 800 within-sample bootstrap resamples are computationally small.
        with TemporaryDirectory() as d,cd(d):
            fixture().to_csv('BBC News Train.csv',index=False)
            ctx=context(d)
            for i in (5,8,21,22,23,25):run_cell(i,ctx)
            self.assertEqual(len(ctx['robustness']),2)
            self.assertEqual(len(ctx['macro_f1_ci']),2)
            self.assertTrue((Path(d)/'08_robustness_stress_test.png').is_file())
            self.assertTrue((Path(d)/'feature_ablation.csv').is_file())
            self.assertTrue((Path(d)/'bootstrap_uncertainty.json').is_file())
            self.assertTrue((Path(d)/'robustness_stress_test.csv').is_file())
            print('Robustness smoke-check completed: NOT BBC results.')

    def test_classification_pipeline_end_to_end_on_synthetic_data(self):
        with TemporaryDirectory() as d,cd(d):
            fixture().to_csv('BBC News Train.csv',index=False)
            ctx=context(d)
            for i in (5,8,21,22,23):run_cell(i,ctx)
            self.assertEqual(len(ctx['cv_df']),4)
            self.assertEqual(ctx['per_class'].shape[0],5)
            self.assertEqual(len(ctx['X_train'])+len(ctx['X_test']),525)
            self.assertTrue(ctx['metrics']['macro_f1']>=0)
            self.assertIn('tfidf',ctx['best_model'].named_steps)
            self.assertEqual(len(ctx['errors']),int((ctx['pred']!=ctx['y_test']).sum()))
            self.assertTrue((Path(d)/'06_confusion_matrix.png').exists())
            print('\nSynthetic smoke-check completed: metrics are NOT BBC results and are NOT published.')

if __name__=='__main__':unittest.main(verbosity=2)
