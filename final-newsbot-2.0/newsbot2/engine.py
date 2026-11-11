"""Coherent API around all four required capstone modules."""
from __future__ import annotations
from collections import Counter
from .schemas import Article
from .retrieval import Retriever
from .analysis import summarize,sentiment,entities,topic_model,headline_suggestions,Classifier
from .language import detect_language,translate_offline
from .chat import Conversation

class NewsBotEngine:
    def __init__(self,articles:list[Article],classifier=None,embedding_model:str|None=None,retrieval_mode:str='tfidf'):
        self.articles=list(articles)
        self.by_id={a.article_id:a for a in self.articles}
        if len(self.by_id)!=len(self.articles):raise ValueError('Duplicate article IDs')
        self.classifier=classifier or Classifier()
        self.retriever=Retriever(self.articles,model_name=embedding_model,retrieval_mode=retrieval_mode)
        self.chat=Conversation(self.retriever)

    def overview(self)->dict:
        return {'total_articles':len(self.articles),
                'label_distribution':dict(Counter(a.category or 'unlabeled' for a in self.articles)),
                'language_hints':dict(Counter(a.language if a.language!='auto' else detect_language(a.full_text)['language'] for a in self.articles)),
                'synthetic_articles':sum(a.synthetic for a in self.articles),
                'retrieval_method':self.retriever.method,
                'classifier_origin':self.classifier.training_origin,
                'data_warning':'Synthetic examples are demos, not real-world validation.'}

    def analyze(self,article_id:str)->dict:
        a=self.by_id[article_id]
        summary=summarize(a.body)
        return {'article':a.to_dict(),'language':detect_language(a.full_text),
                'classification':self.classifier.predict(a.full_text),
                'sentiment':sentiment(a.full_text),'entities':entities(a.full_text),
                'summary':summary,'enhancement':headline_suggestions(a.title,summary['text']),
                'provenance':{'article_id':a.article_id,'sha256':a.sha256,
                              'synthetic':a.synthetic,'source':a.source}}

    def search(self,query:str,k:int=5)->list[dict]:
        return [x.to_dict() for x in self.retriever.search(query,k)]

    def ask(self,question:str)->dict:
        return self.chat.ask(question)

    def topics(self,n_topics:int=4)->dict:
        return topic_model(self.articles,n_topics)

    def train_local_classifier(self)->dict:
        return self.classifier.train(self.articles)

    def translate(self,text:str,src:str,dst:str)->dict:
        return translate_offline(text,src,dst)
