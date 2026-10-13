"""Optional Streamlit dashboard (+5 opportunity subject to instructor grading).
Run notebook first; copy its outputs/newsbot_classifier.joblib into this folder's outputs.
Historical BBC-only model. No factual verification or medical/political advice.
"""
from pathlib import Path
import re
import html
import json
import streamlit as st
import pandas as pd
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from joblib import load
from scipy.special import softmax
import numpy as np

st.set_page_config(page_title='NewsBot Intelligence',page_icon='📰',layout='wide')
DIR=Path(__file__).resolve().parent
OUT=DIR/'outputs'
MODELPATH=OUT/'newsbot_classifier.joblib'
INSIGHTS=OUT/'insights.json'
st.title('NewsBot Intelligence')
st.caption('ITAI 2373 | Historical BBC news NLP | Human review recommended | NOT live news')

@st.cache_resource
def model_load():
    # Only load models created by yourself. joblib/pickle is not safe for unknown files.
    return load(MODELPATH)

@st.cache_resource
def spacy_load():
    return spacy.load('en_core_web_sm')

@st.cache_resource
def vader_load():
    nltk.download('vader_lexicon',quiet=True)
    return SentimentIntensityAnalyzer()

EMOTIONS={
 'joy':{'celebrate','win','success','happy','delight','joy','victory','excite','award','praise'},
 'fear':{'fear','threat','risk','danger','worry','afraid','uncertain','crisis','alarm'},
 'anger':{'anger','angry','outrage','protest','furious','criticize','condemn','rage'},
 'sadness':{'sad','death','loss','grief','mourn','tragic','suffer','disaster'},
 'surprise':{'surprise','unexpected','shock','astonish','sudden','unusual'}}
def linguistic_summary(doc):
    tokens=[w for w in doc if not w.is_space and not w.is_punct]
    pos={tag:round(sum(t.pos_==tag for t in tokens)/max(len(tokens),1),3)
         for tag in ('NOUN','PROPN','VERB','ADJ','ADV','NUM','PRON')}
    lemmas=[w.lemma_.lower() for w in doc if w.is_alpha]
    emotion_hits={name:sum(w in words for w in lemmas) for name,words in EMOTIONS.items()}
    svo=[]
    for w in doc:
        if w.pos_!='VERB':continue
        subjects=[c for c in w.children if c.dep_ in {'nsubj','csubj'}]
        objects=[c for c in w.children if c.dep_ in {'dobj','obj','attr','iobj'}]
        if subjects and objects:svo.append(f'{subjects[0].text} — {w.lemma_} — {objects[0].text}')
    return pos,emotion_hits,svo[:6]

def clean(s):
    s=html.unescape(str(s))
    s=re.sub(r'<[^>]*>',' ',s)
    s=re.sub(r'https?://\S+|www\.\S+',' URL ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

with st.sidebar:
    st.subheader('Dataset boundaries')
    st.write('5 classes: business, entertainment, politics, sport, tech.')
    st.info('Model learned from historical BBC texts. Results are NOT automatically reliable on 2026 articles.')
    st.write('The notebook must be run first using instructor-approved Kaggle training CSV.')
    st.write('Scores from SVM margins are relative display values, **not calibrated probabilities**.')

if not MODELPATH.exists():
    st.error('Missing outputs/newsbot_classifier.joblib. Execute the approved Colab notebook first and copy its model artifact here.')
    st.stop()

try:
    model=model_load();nlp=spacy_load();sia=vader_load()
except Exception as e:
    st.error(f'Model or language resources unavailable: {e}')
    st.code('pip install -r requirements.txt streamlit\npython -m spacy download en_core_web_sm\nstreamlit run dashboard.py')
    st.stop()

if INSIGHTS.exists():
    info=json.loads(INSIGHTS.read_text(encoding='utf-8'))
    m=info.get('evaluation',{})
    c1,c2,c3=st.columns(3)
    c1.metric('Recorded holdout accuracy',f"{100*m.get('holdout',{}).get('accuracy',0):.1f}%")
    c2.metric('Recorded holdout macro-F1',f"{m.get('holdout',{}).get('macro_f1',0):.3f}")
    c3.metric('Trained classifier',m.get('selected_algorithm','Unknown'))

st.subheader('Classify a new English-language article')
title=st.text_input('Title','Fictional tech team announces a new chip')
body=st.text_area('Article text (not an actual breaking-news report)',
    'Engineers unveiled a prototype computing chip for software research. The team said the new processor can run artificial intelligence workloads efficiently. The research prototype was presented at a technical meeting.',height=145)
if st.button('Analyze article',type='primary'):
    if not (title+body).strip():
        st.warning('Please enter some text.')
    else:
        text=clean(title+' '+body)
        predicted=model.predict([text])[0]
        c=model.named_steps['classifier']
        if hasattr(model,'predict_proba'):
            scores=model.predict_proba([text])[0]
            score_type='Model estimated probabilities (not separately calibrated)'
        else:
            scores=softmax(np.atleast_1d(model.decision_function([text])[0]))
            score_type='Relative uncalibrated score from SVM margins; NOT a probability'
        st.success(f'Predicted category: {predicted}')
        st.caption(score_type)
        st.bar_chart(pd.DataFrame({'category':list(c.classes_),'score':scores}).set_index('category'))
        v=sia.polarity_scores(text)
        label='positive' if v['compound']>=.05 else 'negative' if v['compound']<=-.05 else 'neutral'
        st.write('**Lexical sentiment (VADER):**',label,'| compound:',round(v['compound'],3))
        doc=nlp(text[:3500])
        entities=[{'mention':e.text,'type':e.label_} for e in doc.ents if e.label_ in {'PERSON','ORG','GPE','DATE','MONEY'}]
        st.write('**Entities (approximate):**')
        if entities:st.dataframe(pd.DataFrame(entities),use_container_width=True,hide_index=True)
        else:st.info('No target named entities recognized in this article.')
        pos,emotion,svo=linguistic_summary(doc)
        t1,t2,t3=st.tabs(['Grammar/POS','Syntax and emotion','Warnings and method'])
        with t1:
            st.write('**Part of speech proportions (first 3,500 characters)**')
            st.bar_chart(pd.Series(pos).rename('Relative frequency'))
        with t2:
            st.write('**Approximate subject–verb–object patterns**')
            if svo:st.write(' | '.join(svo))
            else:st.info('No simple SVO pattern found; this does not mean the text has no actions.')
            st.write('**Illustrative emotion word hits (not a validated emotion model)**')
            st.bar_chart(pd.Series(emotion).rename('Matching terms'))
        with t3:
            st.warning('Human editorial review required. Classification is trained on old BBC news; text may be from other domains.')
            st.write('VADER polarity does not measure factual truth, author endorsement or political bias. NER and SVO are imperfect annotations; sample tokens are truncated for linguistic features only.')
        st.warning('Editorial review required: reported sentiment ≠ factual validity; names and labels may be inaccurate.')

if INSIGHTS.exists():
    with st.expander('Historical dataset exploratory category insights'):
        st.write('VADER average by BBC topic (descriptive historical sample):')
        st.bar_chart(pd.Series(info.get('sentiment',{}).get('mean_vader_by_category',{}),name='Mean compound'))
        st.json({'dataset':info.get('dataset',{}),'method_limits':info.get('limitations',[])})
        if info.get('class_performance'):
            st.write('**Actual per-category holdout performance**')
            st.dataframe(pd.DataFrame(info['class_performance']),use_container_width=True,hide_index=True)
        if info.get('robustness_stress_test'):
            st.write('**Exploratory within-corpus robustness stress test**')
            st.dataframe(pd.DataFrame(info['robustness_stress_test']),hide_index=True,use_container_width=True)
        st.caption('These plots summarize the historical BBC sample, not contemporary news trends.')
