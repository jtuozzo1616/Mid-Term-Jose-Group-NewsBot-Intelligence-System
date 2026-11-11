"""CPU-first NLP analysis: topic models, classification, sentiment, NER, summaries.
Advanced language assets are optional and never downloaded without explicit setup.
"""
from __future__ import annotations
from collections import Counter
import re
import math
from typing import Any
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize
from .language import detect_language, tokens

POSITIVE={'improve','improved','success','successful','growth','gain','gains','positive','benefit','benefits','safe','support','win','celebrate','advance','progress','mejora','éxito'}
NEGATIVE={'risk','risks','danger','decline','crisis','failure','loss','harm','negative','concern','concerns','threat','warning','delay','pérdida','crise'}
SPLITTER=re.compile(r'(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9])')


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SPLITTER.split(text.strip()) if len(s.strip())>18]


def summarize(text: str, max_sentences: int=3) -> dict[str,Any]:
    """Deterministic extractive centroid summary; quoted source sentences only."""
    sentences=split_sentences(text)[:100]
    if len(sentences)<=max_sentences:
        return {'text':' '.join(sentences) if sentences else text[:500],
                'method':'extractive','selected_sentence_indices':list(range(len(sentences)))}
    try:
        mat=TfidfVectorizer(stop_words='english',ngram_range=(1,2)).fit_transform(sentences)
        import numpy as np
        centroid=normalize(np.asarray(mat.mean(axis=0)))
        scores=np.asarray(mat @ centroid.T).ravel()
        # Partial redundancy penalty prevents near-duplicate sentence selection.
        chosen=[]
        for _ in range(max(1,min(max_sentences,6))):
            options=[]
            for i in range(len(sentences)):
                if i in chosen: continue
                redundancy=max((float((mat[i] @ mat[j].T).toarray()[0,0]) for j in chosen),default=0)
                options.append((float(scores[i])-0.35*redundancy,i))
            chosen.append(max(options)[1])
        chosen.sort()
        return {'text':' '.join(sentences[i] for i in chosen),
                'method':'extractive-centroid-mmr','selected_sentence_indices':chosen}
    except ValueError:
        return {'text':' '.join(sentences[:max_sentences]),'method':'extractive-first-sentences',
                'selected_sentence_indices':list(range(max_sentences))}


def sentiment(text: str) -> dict[str,Any]:
    """Language-specific model is not assumed. English VADER if local lexicon exists."""
    lang=detect_language(text)['language']
    if lang == 'en':
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia=SentimentIntensityAnalyzer() # never silently downloads a lexicon
            compound=float(sia.polarity_scores(text)['compound'])
            return {'label':'positive' if compound>=.05 else 'negative' if compound<=-.05 else 'neutral',
                    'score':round(compound,4),'method':'VADER',
                    'warning':'Lexical tone is not factual truth, bias or author endorsement'}
        except (LookupError,ImportError):
            pass
    t=tokens(text)
    score=(sum(x in POSITIVE for x in t)-sum(x in NEGATIVE for x in t))/max(len(t),1)
    return {'label':'positive' if score>.01 else 'negative' if score<-.01 else 'neutral',
            'score':round(float(score),4),'method':'weak-lexicon-fallback',
            'warning':'Exploratory language-dependent lexical indicator, NOT validated sentiment'}


def entities(text: str) -> dict[str,Any]:
    """spaCy model when installed, else conservative regex candidate mentions."""
    try:
        import spacy
        # spaCy blank pipeline is NOT a trained NER model.
        nlp=spacy.load('en_core_web_sm')
        doc=nlp(text[:10000])
        mentions=[{'text':e.text,'label':e.label_,'start':e.start_char,'end':e.end_char}
                  for e in doc.ents if e.label_ in {'PERSON','ORG','GPE','DATE','MONEY','EVENT'}]
        return {'mentions':mentions[:60],'method':'spacy-en-core-web-sm',
                'warning':'May misidentify names; English-only NER'}
    except (OSError,ImportError):
        matches=list(re.finditer(r'(?<!\w)(?:[A-Z][a-zÀ-ÿ]+\s+){1,3}[A-Z][a-zÀ-ÿ]+',text))
        return {'mentions':[{'text':m.group(0),'label':'PROPER_NAME_CANDIDATE',
                            'start':m.start(),'end':m.end()} for m in matches[:30]],
                'method':'regex-candidates','warning':'Candidate phrases only; not named-entity recognition'}


def headline_suggestions(title: str, summary: str) -> dict[str,Any]:
    """Faithful deterministic content enhancement; no invented quotes or event claims."""
    compact=re.sub(r'\s+',' ',title).strip(' .')[:115]
    return {'headlines':[compact, f'Briefing: {compact}', f'Explainer | {compact}'],
            'short_blurb':summary[:350],
            'guardrail':'Templates preserve user-supplied title; editor must verify accuracy'}


def topic_model(articles: list, n_topics: int=4) -> dict[str,Any]:
    """Unsupervised NMF on current corpus, NOT trained on the test labels."""
    if len(articles)<6:
        return {'status':'insufficient_data','minimum':6}
    try:
        vect=TfidfVectorizer(stop_words='english',max_features=3000,min_df=1,max_df=.95)
        x=vect.fit_transform([a.full_text for a in articles])
        k=min(n_topics,x.shape[0]-1,x.shape[1]-1)
        if k<2: return {'status':'insufficient_vocabulary'}
        nmf=NMF(n_components=k,init='nndsvda',random_state=42,max_iter=350)
        weights=nmf.fit_transform(x)
        feats=vect.get_feature_names_out()
        return {'status':'ok','method':'NMF-TFIDF','topics':[
            {'topic_id':i,'terms':[str(feats[j]) for j in nmf.components_[i].argsort()[-8:][::-1]],
             'article_count_top_topic':int((weights.argmax(axis=1)==i).sum())}
             for i in range(k)],
            'warning':'Topic IDs/terms are exploratory and sensitive to corpus composition'}
    except ValueError as ex:
        return {'status':'unavailable','reason':str(ex)}


class Classifier:
    """Uses trusted midterm artifact if supplied, otherwise abstains unless fitted on labeled local data."""
    def __init__(self, model=None):
        self.model=model
        self.training_origin='not-trained'
        self.labels=[]

    @classmethod
    def from_trusted_joblib(cls, path: str):
        """Explicit trust boundary: NEVER deserialize a file supplied by strangers."""
        import joblib
        model=joblib.load(path)
        obj=cls(model)
        obj.training_origin='historical-BBC-midterm'
        return obj

    def train(self, articles: list) -> dict[str,Any]:
        labeled=[a for a in articles if a.category]
        counts=Counter(a.category for a in labeled)
        if len(labeled)<10 or len(counts)<2 or min(counts.values())<2:
            return {'status':'not_trained','reason':'Need >=10 labeled articles, >=2 classes and >=2 per class'}
        self.model=Pipeline([('tfidf',TfidfVectorizer(stop_words='english',ngram_range=(1,2),max_features=15000)),
                             ('classifier',LogisticRegression(max_iter=1000,random_state=42))])
        self.model.fit([a.full_text for a in labeled],[a.category for a in labeled])
        self.training_origin='current-local-corpus (not externally evaluated)'
        self.labels=sorted(counts)
        return {'status':'trained','training_examples':len(labeled),'training_label_counts':dict(counts),
                'warning':'Training fit is NOT a holdout metric'}

    def predict(self, text: str) -> dict[str,Any]:
        if self.model is None:
            return {'status':'unavailable','label':None,'reason':'No trained classifier loaded'}
        name=str(self.model.predict([text])[0])
        if hasattr(self.model,'predict_proba'):
            scores=self.model.predict_proba([text])[0]
            labels=list(self.model.classes_)
            score_type='model-estimated-probabilities; uncalibrated'
        else:
            import numpy as np
            decision=self.model.decision_function([text])
            if decision.ndim==1: # binary margin
                raw=float(decision[0]); scores=np.array([-raw,raw]); labels=list(self.model.classes_)
            else:
                scores=decision[0]; labels=list(self.model.classes_)
            score_type='SVM-decision-margins; NOT-probabilities'
        ranking=sorted(zip(labels,map(float,scores)),key=lambda x:x[1],reverse=True)
        gap=ranking[0][1]-ranking[1][1] if len(ranking)>1 else 0
        return {'status':'ok','label':name,'ranked_scores':[{'category':k,'score':round(v,4)} for k,v in ranking],
                'score_type':score_type,'top_margin_gap':round(gap,4),
                'training_origin':self.training_origin,
                'warning':'Category suggestion; verify ambiguous and shifted-domain articles'}
