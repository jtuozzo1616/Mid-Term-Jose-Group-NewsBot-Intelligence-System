from fastapi.testclient import TestClient
from newsbot2.api import app
client=TestClient(app)

def test_health_and_overview():
    assert client.get('/health').json()['status']=='ok'
    assert client.get('/overview').json()['total_articles']==30

def test_analysis_unknown_is_404():
    assert client.get('/articles/not-a-real-id/analysis').status_code==404

def test_search_payload_validation():
    assert client.post('/search',json={'query':'x','k':100}).status_code==422
    out=client.post('/search',json={'query':'robot navigation sensors','k':3}).json()
    assert len(out)<=3

def test_chat_reply_has_citations():
    r=client.post('/chat',json={'query':'experimental chip power consumption','k':3})
    assert r.status_code==200
    assert r.json()['status']=='grounded_extract'
