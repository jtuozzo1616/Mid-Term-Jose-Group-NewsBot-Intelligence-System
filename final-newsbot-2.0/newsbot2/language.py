"""Language identification, transparent bilingual lexical pivot, optional offline translation.

Lexicon-based cross-language retrieval is narrow and NOT an MT or semantic equivalence
claim. Production multilingual embeddings require an explicitly installed model.
"""
from __future__ import annotations
from collections import Counter
import re
from typing import Any

STOPWORDS = {
 'en': {'the','and','for','with','from','that','this','will','are','of','to','in','on','by','new','said','was','has','after'},
 'es': {'el','la','los','las','de','del','que','para','con','una','un','en','por','se','fue','nuevo','después','informe'},
 'fr': {'le','la','les','de','des','pour','avec','une','un','dans','est','sur','que','après','nouveau','rapport'},
 'de': {'der','die','das','und','mit','für','eine','ein','von','auf','ist','nach','dem','den','neue','bericht'},
}
# Finite transparent lexicon. Use domain-aligned concepts, NEVER claim general translation.
PIVOT = {
 'tecnologia':'technology','tecnología':'technology','technologie':'technology','technik':'technology',
 'inteligencia':'intelligence','intelligence':'intelligence','künstliche':'artificial','artificial':'artificial',
 'politica':'politics','política':'politics','politique':'politics','politik':'politics',
 'elecciones':'election','elección':'election','élection':'election','wahl':'election',
 'gobierno':'government','gouvernement':'government','regierung':'government',
 'economía':'economy','economia':'economy','économie':'economy','wirtschaft':'economy',
 'mercado':'market','marché':'market','markt':'market','mercados':'market',
 'deportes':'sport','deporte':'sport','sports':'sport','sport':'sport',
 'fútbol':'football','futbol':'football','football':'football','fußball':'football',
 'salud':'health','santé':'health','gesundheit':'health',
 'hospital':'hospital','hôpital':'hospital','krankenhaus':'hospital',
 'clima':'climate','climat':'climate','klima':'climate',
 'energía':'energy','energia':'energy','énergie':'energy','energie':'energy',
 'banco':'bank','banque':'bank','bank':'bank',
 'empresa':'company','entreprise':'company','unternehmen':'company',
 'datos':'data','données':'data','daten':'data',
 'investigación':'research','recherche':'research','forschung':'research',
 'cine':'film','película':'film','peliculas':'film','cinéma':'film','kino':'film',
 'música':'music','musique':'music','musik':'music',
 'robot':'robot','robots':'robot','robotique':'robotics','robótica':'robotics','robotik':'robotics',
 'educación':'education','éducation':'education','bildung':'education',
 'universidad':'university','université':'university','universität':'university',
}

def tokens(text: str) -> list[str]:
    return re.findall(r"[^\W_]+(?:['’-][^\W_]+)*", text.lower(), flags=re.UNICODE)


def detect_language(text: str) -> dict[str, Any]:
    """Language *hint* from stopwords; short text often inconclusive."""
    words=tokens(text)
    count=Counter(words)
    scores={lang:sum(count[w] for w in terms) for lang,terms in STOPWORDS.items()}
    order=sorted(scores, key=lambda x:scores[x], reverse=True)
    best=order[0]
    if scores[best] < 2 or scores[best] == scores[order[1]]:
        return {'language':'und','confidence':'low','method':'stopword-heuristic','scores':scores}
    return {'language':best,'confidence':'medium' if scores[best]>=4 else 'low',
            'method':'stopword-heuristic','scores':scores}


def pivot_terms(text: str) -> str:
    return ' '.join(PIVOT.get(w,w) for w in tokens(text))


def translate_offline(text: str, source: str, target: str) -> dict[str, Any]:
    """Translate with local Argos language packs only; never silently use a paid API."""
    if source == target:
        return {'status':'identity','translated_text':text,'provider':'none'}
    try:
        from argostranslate import translate
        langs=translate.get_installed_languages()
        src=next((x for x in langs if x.code==source),None)
        dst=next((x for x in langs if x.code==target),None)
        if src and dst:
            tr=src.get_translation(dst)
            if tr:
                return {'status':'ok','translated_text':tr.translate(text),
                        'provider':'argos-local','caveat':'Check translations of names and quotes'}
    except (ImportError,Exception) as exc:
        # All translator/configuration failures are surfaced as unavailability,
        # not replaced by fabricated text.
        return {'status':'unavailable','translated_text':None,'provider':'argos-local',
                'reason':f'Argos or language pack unavailable: {type(exc).__name__}'}
    return {'status':'unavailable','translated_text':None,'provider':'argos-local',
            'reason':f'No installed {source}->{target} translation package'}
