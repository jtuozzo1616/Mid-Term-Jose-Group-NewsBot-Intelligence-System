"""Evidence-first retrieval; quoted snippets and stable [article_id] citations."""
from __future__ import annotations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from .language import pivot_terms
from .analysis import split_sentences
from .schemas import SearchHit, Article

class Retriever:
    def __init__(self, articles: list[Article], model_name: str | None=None, retrieval_mode: str='tfidf'):
        self.articles=list(articles)
        self.model_name=model_name
        if retrieval_mode not in {'tfidf','lsa'}:raise ValueError('retrieval_mode must be tfidf or lsa')
        self.retrieval_mode=retrieval_mode
        self.svd=None
        self.embedding_model=None
        self.vectors=None
        self.vectorizer=None
        self.method='tfidf-pivot'
        if not self.articles:
            return
        if model_name: # explicitly opted in; might download large weights
            try:
                from sentence_transformers import SentenceTransformer
                self.embedding_model=SentenceTransformer(model_name)
                self.vectors=self.embedding_model.encode([a.full_text for a in articles],
                                                           normalize_embeddings=True)
                self.method=f'multilingual-embeddings:{model_name}'
            except (ImportError, OSError, RuntimeError):
                self.embedding_model=None
        if self.embedding_model is None:
            self.vectorizer=TfidfVectorizer(ngram_range=(1,2),stop_words='english',
                                              sublinear_tf=True,strip_accents='unicode')
            self.vectors=self.vectorizer.fit_transform([pivot_terms(a.full_text) for a in articles])
            if retrieval_mode == 'lsa' and len(articles)>=4:
                n=min(64,self.vectors.shape[0]-1,self.vectors.shape[1]-1)
                if n>=2:
                    self.svd=TruncatedSVD(n_components=n,random_state=42)
                    self.vectors=normalize(self.svd.fit_transform(self.vectors))
                    self.method='lsa-svd-pivot'

    def search(self, query: str, k:int=5, language: str|None=None) -> list[SearchHit]:
        if not self.articles or not query.strip(): return []
        if self.embedding_model:
            q=self.embedding_model.encode([query],normalize_embeddings=True)
            scores=(self.vectors @ q[0]).ravel()
        else:
            q=self.vectorizer.transform([pivot_terms(query)])
            if self.svd is not None:
                q=normalize(self.svd.transform(q))
            scores=cosine_similarity(q,self.vectors).ravel()
        order=sorted(range(len(scores)),key=lambda i:(-float(scores[i]),self.articles[i].article_id))
        hits=[]
        for i in order[:max(1,min(k,20))]:
            score=float(scores[i]); a=self.articles[i]
            if score<=0.000001: continue
            sentences=split_sentences(a.body)
            # Snippet is verbatim content, not a generated or rephrased 'quote'.
            excerpt=' '.join(sentences[:2])[:390] if sentences else a.body[:390]
            hits.append(SearchHit(a.article_id,a.title,round(score,4),excerpt,
                                  a.source,a.synthetic,self.method))
        return hits
