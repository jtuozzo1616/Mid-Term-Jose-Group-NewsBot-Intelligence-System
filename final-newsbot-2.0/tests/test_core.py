"""Offline tests: behavior, safety boundaries, provenance and regression."""
from pathlib import Path
import pytest
from newsbot2.schemas import Article,normalize_text
from newsbot2.io import import_articles
from newsbot2.engine import NewsBotEngine
from newsbot2.analysis import summarize,topic_model,Classifier
from newsbot2.language import detect_language,pivot_terms,translate_offline
from newsbot2.evaluation import evaluate_classification_cv,evaluate_retrieval

HERE=Path(__file__).resolve().parents[1]
@pytest.fixture(scope='module')
def corpus():return import_articles(HERE/'data/demo_news.jsonl')
@pytest.fixture(scope='module')
def engine(corpus):return NewsBotEngine(corpus)

def test_demo_data_are_fictional(corpus):
    assert len(corpus)==30
    assert all(a.synthetic for a in corpus)
    assert len({a.article_id for a in corpus})==30
    assert len({a.category for a in corpus})==5

def test_article_validation():
    with pytest.raises(ValueError):Article('bad/path','Hi','Some sufficiently lengthy story about an example article.')
    with pytest.raises(ValueError):Article('valid','Title','short')
    with pytest.raises(ValueError):Article('valid','Title','An example body with enough text to satisfy validation.','x',url='file:///etc/passwd')

def test_normalization():
    assert '<script>' not in normalize_text('<script>alert(1)</script>')
    assert normalize_text(' hello\n world ')=='hello world'

def test_corpus_statistics(engine):
    s=engine.overview()
    assert s['total_articles']==30
    assert s['synthetic_articles']==30
    assert s['label_distribution']['tech']==6

def test_analysis_provenance(engine):
    out=engine.analyze('demo-tech-1')
    assert out['provenance']['synthetic']
    assert len(out['provenance']['sha256'])==64
    assert out['summary']['text']
    assert 'method' in out['sentiment']
    assert out['classification']['status']=='unavailable'

def test_summarizer_extracts_only_original_sentences():
    text='Alpha researchers test a new system. The study gathers observations during laboratory experiments. Researchers evaluate the collected observations carefully. An additional study is planned for next month.'
    summary=summarize(text,2)
    assert summary['method'].startswith('extractive')
    assert len(summary['selected_sentence_indices'])==2
    for sentence in summary['text'].split('. '):
        assert sentence.rstrip('.') in text

def test_search_produces_real_source_id(engine):
    hits=engine.search('robot navigation sensors',k=5)
    assert hits
    assert hits[0]['article_id'] in engine.by_id
    assert hits[0]['retrieval_method']=='tfidf-pivot'
    assert all(h['synthetic'] for h in hits)

def test_cross_language_keyword_bridge(engine):
    hits=engine.search('robótica tecnología investigación',k=10)
    assert hits
    assert 'robotics' in pivot_terms('robótica')

def test_grounding_and_citations(engine):
    reply=engine.ask('AI chip energy laboratory')
    assert reply['status']=='grounded_extract'
    assert reply['citations']
    for citation in reply['citations']:
        assert citation['article_id'] in engine.by_id
        assert f"[{citation['article_id']}]" in reply['answer']

def test_unsupported_question_abstains(engine):
    reply=engine.ask('quasar zxqv 98877 elephantine teleportation')
    assert reply['status']=='insufficient_evidence'
    assert not reply['citations']

def test_language_not_overconfident():
    assert detect_language('123!?')['language']=='und'
    assert detect_language('el informe de la universidad con una investigación')['language']=='es'

def test_uninstalled_translation_never_fabricates():
    r=translate_offline('Hola mundo','es','en')
    assert r['status'] in {'ok','unavailable'}
    assert (r['translated_text'] is None) if r['status']=='unavailable' else isinstance(r['translated_text'],str)

def test_topic_output(engine):
    t=engine.topics(5)
    assert t['status']=='ok'
    assert len(t['topics'])==5
    assert all(len(x['terms'])>0 for x in t['topics'])

def test_cv_provenance(corpus):
    result=evaluate_classification_cv(corpus,3)
    assert result['status']=='ok'
    assert result['n_articles']==30
    assert result['method'].startswith('3-fold stratified')
    assert 0<=result['macro_f1']<=1
    assert 'synthetic' in result['limitation']

def test_local_training_is_not_a_metric(engine):
    result=engine.train_local_classifier()
    assert result['status']=='trained'
    pred=engine.classifier.predict('AI chip robotics and sensors used in research')
    assert pred['status']=='ok'
    assert 'uncalibrated' in pred['score_type']

def test_import_rejects_duplicate(tmp_path):
    from newsbot2.io import export_jsonl
    a=Article('dup','One','This is a sufficiently long synthetic story body example.')
    f=tmp_path/'x.jsonl';export_jsonl([a,a],f)
    with pytest.raises(ValueError,match='Duplicate'):import_articles(f)

def test_retrieval_evaluation(engine):
    r=evaluate_retrieval(engine,[('low power artificial intelligence chips','demo-tech-1')],k=5)
    assert r['queries']==1
    assert r['recall_at_k']==1


def test_follow_up_resolves_prior_citation(engine):
    e=NewsBotEngine(engine.articles)
    first=e.ask('robot navigation sensors')
    assert first['citations']
    second=e.ask('Tell me more about that story')
    assert 'resolved_query' in second
    assert e.by_id[first['citations'][0]['article_id']].title in second['resolved_query']

def test_duplicate_clustering_flags_repeated_story():
    from newsbot2.research import duplicate_clusters
    a=Article('a','University team tests robotics','A university team tests robotics in the lab with cameras and sensors for navigation.')
    b=Article('b','University team tests robotics','A university team tests robotics in the lab with cameras and sensors for navigation.')
    c=Article('c','Other film documentary','A filmmaker created a new documentary about music, culture and local art.')
    result=duplicate_clusters([a,b,c],.75)
    assert ['a','b'] in result['clusters']
    assert 'c' not in result['clusters'][0]


def test_cpu_lsa_search(corpus):
    alt=NewsBotEngine(corpus,retrieval_mode='lsa')
    assert alt.retriever.method=='lsa-svd-pivot'
    hits=alt.search('robot navigation sensors',k=3)
    assert len(hits)>=1
    assert hits[0]['article_id'] in alt.by_id
