"""Conversational evidence synthesis, not an ungrounded generative chat completion."""
from __future__ import annotations
from typing import Any
from .analysis import summarize,split_sentences
from .language import detect_language

GREETINGS={'hi','hello','hey','hola','bonjour','hallo'}

class Conversation:
    def __init__(self, retriever, max_turns:int=12):
        self.retriever=retriever
        self.max_turns=max_turns
        self.history=[]

    def ask(self, question:str, top_k:int=3)->dict[str,Any]:
        q=question.strip()[:1000]
        if not q:
            return {'status':'clarify','answer':'Please enter a question.','citations':[]}
        if q.lower().rstrip('!? .') in GREETINGS:
            return {'status':'greeting','answer':'Ask me about articles in the loaded corpus. I will cite the evidence I use.','citations':[]}
        # Resolve explicitly anaphoric follow-ups against the last cited article.
        # The expansion is visible to the caller and uses only corpus metadata.
        effective_query=q
        refs=(self.history[-1].get('citations',[]) if self.history else [])
        anaphoric=('what about it','what happened next','tell me more','and that','those articles','that story',
                   'what about this','more on that','y sobre eso','cuéntame más',"qu'en est-il",'erzähl mehr')
        if refs and any(term in q.lower() for term in anaphoric):
            ref_id=refs[0]
            match=next((a for a in self.retriever.articles if a.article_id==ref_id),None)
            if match:effective_query=q+' '+match.title
        hits=self.retriever.search(effective_query,k=top_k)
        # A question cannot be answered from a corpus without overlapping evidence.
        if not hits or hits[0].score<.025:
            answer=('I could not find adequate supporting material in the loaded articles. '
                    'Please name a topic, entity or article title, or upload relevant sources.')
            result={'status':'insufficient_evidence','answer':answer,'citations':[],
                    'retrieval_method':self.retriever.method,'confidence_policy':'abstain-on-low-retrieval'}
        else:
            # Keep only candidates close to the best source, not calibrated answer confidence.
            cutoff=max(.025, .50 * hits[0].score)
            supported=[hit for hit in hits if hit.score>=cutoff][:3]
            blocks=[]
            for hit in supported:
                blocks.append(f'[{hit.article_id}] {hit.excerpt[:390]}')
            result={'status':'grounded_extract','answer':'\n\n'.join(blocks),
                    'citations':[{'article_id':h.article_id,'title':h.title,'source':h.source,
                                  'retrieval_score':h.score,'synthetic':h.synthetic} for h in supported],
                    'retrieval_method':self.retriever.method,
                    'confidence_policy':'retrieval-score-only (not calibrated answer probability)',
                    'warning':'These excerpts come from source texts; they are not independently fact-checked.'}
        result['resolved_query']=effective_query
        self.history=(self.history+[{'question':q,'result':result['status'],
                                    'citations':[x['article_id'] for x in result.get('citations',[])]}])[-self.max_turns:]
        return result
