"""Optional advanced research: near-duplicate discovery via cosine graph components."""
from __future__ import annotations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def duplicate_clusters(articles,threshold:float=.75)->dict:
    if not .4 <= threshold <= 1:raise ValueError('threshold must be between 0.4 and 1')
    if not articles:return {'status':'ok','clusters':[],'threshold':threshold}
    x=TfidfVectorizer(ngram_range=(1,2),strip_accents='unicode').fit_transform([a.full_text for a in articles])
    scores=cosine_similarity(x)
    parent=list(range(len(articles)))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        ri,rj=root(i),root(j)
        if ri!=rj:parent[max(ri,rj)]=min(ri,rj)
    pairs=[]
    for i in range(len(articles)):
        for j in range(i+1,len(articles)):
            if float(scores[i,j])>=threshold:
                union(i,j);pairs.append({'left':articles[i].article_id,'right':articles[j].article_id,
                                         'similarity':round(float(scores[i,j]),4)})
    groups={}
    for i,a in enumerate(articles):groups.setdefault(root(i),[]).append(a.article_id)
    return {'status':'ok','threshold':threshold,'clusters':[v for v in groups.values() if len(v)>1],
            'candidate_pairs':pairs,
            'warning':'Similarity groups are editorial review candidates, not proof of duplication'}
