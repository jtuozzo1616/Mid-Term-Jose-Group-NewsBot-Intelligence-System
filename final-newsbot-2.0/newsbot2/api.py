"""Optional typed HTTP endpoints; reads local demo corpus only, no remote fetching."""
from functools import lru_cache
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from .engine import NewsBotEngine
from .io import import_articles

app=FastAPI(title='NewsBot Intelligence System 2.0',version='2.0.0',
            description='Local-first grounded news analysis. Demo data are synthetic.')
DATA=Path(__file__).resolve().parent.parent/'data'/'demo_news.jsonl'

@lru_cache(maxsize=1)
def engine():
    return NewsBotEngine(import_articles(DATA))

class QueryRequest(BaseModel):
    query:str=Field(min_length=2,max_length=1000)
    k:int=Field(default=5,ge=1,le=10)

@app.get('/health')
def health(): return {'status':'ok','mode':'synthetic-demo','version':'2.0.0'}

@app.get('/overview')
def overview(): return engine().overview()

@app.get('/articles')
def articles():
    return [{'article_id':a.article_id,'title':a.title,'source':a.source,'synthetic':a.synthetic} for a in engine().articles]

@app.get('/articles/{article_id}/analysis')
def analyze(article_id:str):
    if article_id not in engine().by_id:raise HTTPException(404,'Unknown article ID')
    return engine().analyze(article_id)

@app.post('/search')
def search(req:QueryRequest): return engine().search(req.query,req.k)

@app.post('/chat')
def chat(req:QueryRequest):
    from .chat import Conversation
    # Stateless HTTP requests: avoid sharing chat history across API clients.
    return Conversation(engine().retriever).ask(req.query,req.k)

@app.get('/topics')
def topics(n:int=Query(4,ge=2,le=8)): return engine().topics(n)
