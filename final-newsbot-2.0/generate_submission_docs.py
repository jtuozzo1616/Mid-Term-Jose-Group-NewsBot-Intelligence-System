"""Create instructor-friendly PDF documents from verified release results.
This generator is included for reproducibility; PDFs use provisional group naming.
"""
from __future__ import annotations
from datetime import date
import json,math
from pathlib import Path
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT,TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether,Image,HRFlowable
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
DOC=ROOT/'docs';DOC.mkdir(exist_ok=True)
ART=ROOT/'artifacts'
results=json.loads((ART/'research_results.json').read_text())
metrics=results['synthetic_classification_cv']
probe=results['retrieval_probes']

NAVY=colors.HexColor('#14243A'); TEAL=colors.HexColor('#087E84')
SLATE=colors.HexColor('#57677A'); LGRAY=colors.HexColor('#E9EFF3'); WHITE=colors.white
GOLD=colors.HexColor('#BB7D34'); DARK=colors.HexColor('#23344B')

# Use installed fonts; never distribute font files.
font_regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if Path(font_regular).exists():
    pdfmetrics.registerFont(TTFont('DejaVu',font_regular))
    pdfmetrics.registerFont(TTFont('DejaVuBold',font_bold))
    FN='DejaVu';FB='DejaVuBold'
else:FN='Helvetica';FB='Helvetica-Bold'

ST={
 'eyebrow':ParagraphStyle('eyebrow',fontName=FB,fontSize=8.5,leading=12,textColor=TEAL,spaceAfter=7),
 'cover':ParagraphStyle('cover',fontName=FB,fontSize=29,leading=38,textColor=NAVY,spaceAfter=15),
 'subtitle':ParagraphStyle('subtitle',fontName=FN,fontSize=12.5,leading=20,textColor=SLATE,spaceAfter=15),
 'h1':ParagraphStyle('h1',fontName=FB,fontSize=16,leading=22,textColor=NAVY,spaceBefore=20,spaceAfter=10,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName=FB,fontSize=10.6,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'body':ParagraphStyle('body',fontName=FN,fontSize=8.8,leading=14.9,textColor=DARK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName=FN,fontSize=7.35,leading=11.5,textColor=SLATE,spaceAfter=6),
 'bullet':ParagraphStyle('bullet',fontName=FN,fontSize=8.7,leading=13.8,textColor=DARK,leftIndent=15,firstLineIndent=-10,spaceAfter=5),
 'tbl':ParagraphStyle('tbl',fontName=FN,fontSize=7.25,leading=10.7,textColor=DARK),
 'th':ParagraphStyle('th',fontName=FB,fontSize=7.2,leading=10.2,textColor=WHITE),
 'quote':ParagraphStyle('quote',fontName=FN,fontSize=9,leading=15,textColor=TEAL,spaceBefore=8,spaceAfter=8,leftIndent=16,rightIndent=12),
}

def P(s,kind='body'):
    from xml.sax.saxutils import escape
    # Source paragraphs are authored with intentionally minimal HTML markup, not untrusted data.
    return Paragraph(s,ST[kind])

def bullet(s):return P('• '+s,'bullet')

def T(data,widths=None):
    rows=[[P(str(v),'th' if i==0 else 'tbl') for v in row] for i,row in enumerate(data)]
    t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,colors.HexColor('#F5F8FA')]),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('LINEBELOW',(0,-1),(-1,-1),.6,LGRAY),
    ]))
    return t

def on_page(canvas,doc):
    canvas.saveState();w,h=letter
    canvas.setFillColor(NAVY);canvas.rect(0,h-15,w,15,fill=1,stroke=0)
    canvas.setFont(FB,7.1);canvas.setFillColor(TEAL)
    canvas.drawString(43,h-36,'NEWSBOT INTELLIGENCE 2.0  /  ITAI 2373')
    canvas.setStrokeColor(LGRAY);canvas.line(43,43,w-43,43)
    canvas.setFillColor(SLATE);canvas.setFont(FN,7)
    canvas.drawString(43,30,'ACADEMIC CAPSTONE  ·  NOVEMBER 2026')
    canvas.drawRightString(w-43,30,f'Page {doc.page}')
    canvas.restoreState()

def create(name,story):
    p=DOC/name
    doc=SimpleDocTemplate(str(p),pagesize=letter,rightMargin=43,leftMargin=43,topMargin=58,bottomMargin=57,
                          title='NewsBot Intelligence System 2.0',author='José Miguel Tuozzo Izaguirre',
                          subject='ITAI 2373 final project technical materials')
    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    return p

# Visuals for real measured synthetic probe scores. Matplotlib assets are part of the project.
fig,ax=plt.subplots(figsize=(7.5,2.65))
fig.patch.set_facecolor('white')
ax.barh(['Without bilingual pivot','With bilingual pivot'],[probe['naive_mrr'],probe['pivot_mrr']],color=['#7E8EA2','#087E84'],height=.5)
ax.set_xlim(0,1.08);ax.set_xlabel('Mean reciprocal rank @ 3 | 24 synthetic queries',fontsize=9)
ax.grid(axis='x',alpha=.18)
ax.set_axisbelow(True)
for i,v in enumerate([probe['naive_mrr'],probe['pivot_mrr']]):ax.text(v+.014,i,f'{v:.3f}',va='center',fontsize=10,fontweight='bold')
for spine in ax.spines.values():spine.set_visible(False)
fig.tight_layout();fig.savefig(ART/'retrieval_ablation.png',dpi=160,bbox_inches='tight');plt.close(fig)

TECH='FP_TechnicalDoc_JoseMiguelTuozzo_JoseGroup_ITAI2373.pdf'
EXEC='FP_ExecutiveSummary_JoseMiguelTuozzo_JoseGroup_ITAI2373.pdf'
REFL='FP_ReflectiveJournal_JoseGroup_ITAI2373.pdf'

story=[Spacer(1,46),P('FINAL CAPSTONE  ·  TECHNICAL DOCUMENTATION','eyebrow'),
       P('NewsBot Intelligence<br/>System 2.0','cover'),
       P('An evidence-first, CPU-capable NLP platform for explainable article analysis, multilingual discovery and source-grounded conversation.','subtitle'),
       HRFlowable(width='100%',thickness=3,color=TEAL),Spacer(1,17),
       T([['STUDENT','COURSE','RELEASE'],['José Miguel Tuozzo Izaguirre','Houston Community College | ITAI 2373','2.0.0 · November 2026']],widths=[190,202,134]),
       Spacer(1,18),P('<b>Submission context:</b> final project due December 1, 2026. Project extends the existing NewsBot Intelligence System midterm repository. Team name <b>JoseGroup</b> is provisional; confirm Canvas group details.','body'),
       P('<b>Evidence classification:</b> independent historical BBC midterm figures are not NewsBot 2.0 test scores. This release contains a 30-item synthetic corpus and a 24-query controlled ablation; neither measures real newsroom quality.','body'),
       Spacer(1,25),P('TECHNICAL DOCUMENT CONTENTS','eyebrow'),
       P('01  Executive scope and lineage<br/>02  System architecture and data flow<br/>03  Four required NLP modules<br/>04  Experimental design and results<br/>05  Source grounding and reliability<br/>06  Software engineering, API and testing<br/>07  Threats, ethics and deployment boundaries<br/>08  Roadmap, limitations and references','body'),
       PageBreak()]

story += [P('01 / Problem statement and inherited midterm','h1'),
P('Editors, researchers and students often need to sort, examine, retrieve and understand large collections of articles. A useful assistant must do more than return a plausible category: it must preserve provenance, avoid presenting lexical sentiment as verified facts and abstain when source support is missing.'),
P('The prior midterm implementation analyzed historical BBC news from 2004–2005 with eight modules: data preparation, preprocessing, TF-IDF, POS tagging, syntax, sentiment, classification and named entities. Its evaluated Linear SVM achieved <b>96.18% accuracy (277/288)</b> and <b>0.9605 macro-F1</b> on the reserved in-domain BBC holdout. That result is inherited reference evidence only, not a metric for this new system.'),
P('The capstone transforms the earlier notebook-oriented investigation into an importable, modular NLP library with a web interface, REST API, command-line workflows, multilingual options, structured evaluation and tests. No paid generative API is required for the standard local demonstration.'),
P('02 / Architecture and data movement','h1'),
T([['STAGE','INPUT → OUTPUT','CONTROL / EVIDENCE'],
   ['Ingestion','CSV / JSONL → validated Article objects','File and text size bounds; safe IDs; source and synthetic markers'],
   ['Language layer','Article/query → language hint + bilingual pivot','Low-signal text returns undetermined; glossary bounds disclosed'],
   ['Analysis','Text → category, topics, tone, entities, summary','Trusted models, method tags, exact sentence positions'],
   ['Retrieval','Question → sparse or embedding similarity ranking','Stable document IDs and uncalibrated retrieval scores'],
   ['Grounded chat','Top results → verbatim quoted passages','Article citations, no-evidence abstention, follow-up context'],
   ['Interaction','Core engine → Streamlit / FastAPI / CLI','Editable corpus, visible provenance, repeatable API calls']],widths=[99,198,229]),
P('The system is local-first: inputs are not sent to a remote LLM. Optional Argos language packs and Sentence Transformers weights may be installed separately for genuinely multilingual translation or embedding retrieval. The fallback is deliberately narrower and visibly labeled.'),
P('03 / Module I — Advanced Content Analysis Engine','h1'),
P('<b>Classification.</b> The class supports a trusted local midterm joblib artifact if the file exists. Otherwise a trainable TF-IDF + Logistic Regression pipeline fits user-provided labeled documents, clearly marked as a locally trained model. Predicted labels and ranked scores are not automatically treated as calibrated confidence. Real validation requires frozen splits.'),
P('<b>Topic modeling.</b> Nonnegative Matrix Factorization decomposes the current document-term TF-IDF matrix, and returns an interpretable list of dominant terms plus document-count assignments. Topic IDs are descriptive and will vary with corpus composition.'),
P('<b>Sentiment and entities.</b> VADER is used if English-language lexicon resources exist. Otherwise the fallback is an explicitly weak word-list score; no moral judgment, factual verification or political-bias score is inferred. English spaCy NER is optional; absent model weights, candidate proper-name phrases are labeled as candidates, not entities.'),
P('No automatic story publication, fact-check verdict, or editorial override is performed by this module.'),
]

story += [P('03 / Module II — Language Understanding & Generation','h1'),
P('The summarizer splits input text into original sentences, constructs a TF-IDF centroid and greedily selects high-relevance sentences with redundancy suppression, preserving their original order. It reports exact selected sentence indices. The resulting text is extractive and traceable rather than a potentially hallucinated paraphrase.'),
P('The content-enhancement function proposes conservative headline variants and a short article blurb. This is <b>template-based editorial assistance</b>, not an installed generative language model. Editorial verification remains necessary, particularly where quoted statements, uncertainty or ambiguous actors are involved.'),
P('TF-IDF retrieval indexes documents using unigrams and bigrams; it returns similarity-ranked source IDs with excerpts. If opted in, `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` replaces the lexical retrieval path with learned multilingual embeddings. That optional execution mode requires installing and caching model weights and is not counted as a verified default-path experiment.'),
P('03 / Module III — Multilingual Intelligence','h1'),
P('The base engine uses a transparent English/Spanish/French/German stopword heuristic to provide a language <i>hint</i>; low-evidence cases return `und`. Its finite translation-equivalent vocabulary enables basic cross-language keyword matching, but it cannot produce complete translations or reliably infer sentence semantics. Optional Argos Translate integrates with installed offline translation language packs and otherwise returns `status=unavailable`. No fabricated translation is generated.'),
P('A research ablation explicitly tests how the constrained pivot affects retrieval ranking on hand-authored synthetic probes. These probes were curated from the same fictional corpus; the improvement is instructional evidence, not a multilingual benchmark score.'),
P('03 / Module IV — Conversational Interface','h1'),
P('The question-answer system performs retrieval and cites the original article IDs, such as `[demo-tech-1]`. The actual answer consists of source excerpts. It records a bounded conversation history and expands certain follow-up phrases using the preceding cited article title; the expanded query is exposed in `resolved_query` to support an audit. Requests without adequate lexical match return a clarification request instead of unsupported assertions.'),
P('<b>Honesty boundary:</b> a cited article can itself be inaccurate, fictional or outdated. Citation means traceability to ingested content, not independent verification of its factual claims.'),
P('04 / Evaluation materials and experiment provenance','h1'),
P('The bundled evaluation set contains <b>30 hand-authored fictional articles</b>, balanced across five topics (6 each), with language-marked English, Spanish, French and German examples. The research script uses <b>24 deliberately authored queries</b>, including bilingual dictionary probes. Some probes were chosen after exploring corpus vocabulary, so the result is not an untouched benchmark.'),
T([['EVIDENCE / METRIC','OBSERVED VALUE','INTERPRETATION'],
   ['Historical BBC midterm holdout','Accuracy 0.9618; macro-F1 0.9605','Prior notebook; historical, English, single publisher'],
   ['NewsBot 2.0 synthetic CV',f"Accuracy {metrics['accuracy']:.4f}; macro-F1 {metrics['macro_f1']:.4f}",'3-fold, 30 fictional articles; not deployment estimate'],
   ['Retrieval MRR@3 with pivot',f"{probe['pivot_mrr']:.4f}",'24 hand-authored queries on authored corpus'],
   ['Retrieval MRR@3 without pivot',f"{probe['naive_mrr']:.4f}",'Matched TF-IDF baseline, no glossary pivot'],
   ['Automated tests','25 passing in local container','Offline functional and API contract tests']],widths=[152,153,221]),
Image(str(ART/'retrieval_ablation.png'),width=500,height=181),
P('Figure 1. Hand-authored synthetic retrieval ablation. Higher MRR is better; this experiment has no independent external test set.','small'),
]

story += [P('04 / Evaluation reproducibility and diagnostics','h1'),
P('<b>Recipe:</b> install `requirements-dev.txt`; run `python -m pytest tests -q`; run `python run_research.py`. The script writes `artifacts/research_results.json` with input identifiers, SHA-256 fingerprints, software metadata, individual query ranks, complete confusion matrix and per-class scores. No test set is quietly substituted for production articles.'),
P('Macro-F1 is informative for category-balanced reporting; the synthetic cross-validation score is low compared with historical BBC because the toy corpus is tiny and multilingual. The demo therefore illustrates the need for adequate training data and independent domain testing, not a reason to hide poor numbers.'),
P('In an actual evaluation, source-separated and time-separated holdouts would test topic and publisher shift; per-language performance would expose uneven multilingual results; question answerability should measure citation support; and calibrated uncertainty thresholds would be tuned on validation data, never retrofitted to the final test set.'),
P('05 / Explainability and human oversight','h1'),
T([['POTENTIAL OUTPUT','EVIDENCE THAT MUST BE SHOWN','ALLOWED CLAIM'],
    ['Category','Model identity, training origin, scores/labels','Suggested editorial routing, not verified truth'],
    ['Topic terms','NMF terms and assigned document counts','Corpus-specific thematic structure'],
    ['Tone','VADER or weak lexical method','Surface language polarity only'],
    ['Named entities','spaCy model or candidate regex method','Unverified proper-noun extraction'],
    ['Summary','Verbatim source sentences and indices','Extractive evidence digest'],
    ['Answer','Article IDs + source excerpts','Text supported by ingested sources'],
    ['Translation','Argos status and installed model availability','Translation only if actual local pack succeeded']],widths=[111,208,207]),
P('Every response with weak support should invite the user to provide a clearer question or more source material. This conservative design is appropriate for a free classroom environment and prevents paid API limitations from breaking core functionality.'),
P('06 / Engineering quality, interface and API','h1'),
P('The codebase separates input schemas, language functions, analysis, search, chat, orchestration and evaluation. Data import validates identifiers, file size (8 MB), corpus size (3,000 items), supported formats and duplicate IDs. The FastAPI schema bounds question length and top-K. The Streamlit UI uses per-session engine state; the HTTP chat endpoint is stateless to avoid exposing conversation history across clients.'),
P('The web interface has five practical workspaces: Command Center, Article Lab, Search & Languages, Grounded Chat and Research Lab. API documentation is available via `/docs` when FastAPI is running. Unit/API regression tests cover input rejection, article evidence, topic modeling, follow-ups, abstention and repeatable research.'),
P('The Streamlit frontend source is included for the 30-point bonus opportunity; it was syntax-checked but <b>not independently browser-tested or publicly hosted</b> in this execution environment. The exact bonus is determined by the instructor.'),
]

story += [P('07 / Security, governance and limitations','h1'),
P('The current system is a <b>production-oriented academic prototype</b>. It is not an authenticated, monitored newsroom deployment. API users can read the bundled synthetic dataset; hosting the service on the public internet without access controls, resource quotas and logging policies is not recommended.'),
T([['RISK','CURRENT MITIGATION','REQUIRED FOR LIVE DEPLOYMENT'],
['Unsupported or malicious claims','Only source excerpts; no LLM prompts executed','Fact checking and editorial signoff'],
['Prompt injection','Retrieved text is treated as data, not instructions','Red-team testing before introducing generative LLMs'],
['Model leakage / serialized code','Only manually chosen trusted local joblib','Signed artifacts and dependency scanning'],
['Drift and language errors','Explicit domain and model labels','Representative year/language/publisher holdouts'],
['Access and infrastructure','Local-first, bounded import/query sizes','Authentication, rate limits, encryption, monitoring'],
['Copyright/privacy','Only fictional default text; no remote fetch','Source licenses, retention/deletion governance']],widths=[126,185,215]),
P('08 / Evidence-first roadmap','h1'),
bullet('Acquire licensed multi-publisher, date-stamped English and non-English corpora; document the sampling plan.'),
bullet('Freeze data splits by publisher and date; evaluate multilingual embeddings against the pivot baseline with predefined queries.'),
bullet('Collect independently rated sentiment, NER, extractive summary and answer citation annotations.'),
bullet('Add calibrated classification scores, explicit abstention calibration, out-of-distribution checks and human-review measurements.'),
bullet('Deploy a staged service with authentication, resource limits, observability, privacy policy and a genuine newsroom pilot.'),
P('References / implementation notes','h1'),
P('Original midterm repository: https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System','small'),
P('scikit-learn text feature extraction: https://scikit-learn.org/stable/modules/feature_extraction.html','small'),
P('Sentence Transformers multilingual models: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html','small'),
P('Argos Translate docs: https://argos-translate.readthedocs.io/en/stable/index.html','small'),
P('Streamlit chat API: https://docs.streamlit.io/develop/api-reference/chat','small'),
P('FastAPI docs: https://fastapi.tiangolo.com/','small')]
p1=create(TECH,story)

exec_story=[Spacer(1,35),P('FINAL PROJECT  /  EXECUTIVE SUMMARY','eyebrow'),
 P('From classification notebook<br/>to intelligence workspace','cover'),
 P('NewsBot Intelligence System 2.0 | ITAI 2373','subtitle'),
 HRFlowable(width='100%',thickness=3,color=TEAL),Spacer(1,15),
 P('THE OPPORTUNITY','eyebrow'),
 P('Editors and research teams need more than simple keyword categorization. They need to explore collections across languages, see what evidence supports each answer and understand when a model is uncertain. NewsBot 2.0 demonstrates a practical response: a modular NLP research workspace with traceable article identifiers.'),
 P('THE SOLUTION','eyebrow'),
 T([['CORE CAPABILITY','HOW NEWSBOT 2.0 ADDRESSES IT'],
 ['Advanced article intelligence','Category suggestions, NMF topic modeling, sentiment and entity extraction'],
 ['Understanding and synthesis','Extractive multi-sentence summaries, source links, conservative headlines'],
 ['Multilingual discovery','EN/ES/FR/DE glossary-assisted retrieval; opt-in embeddings and Argos packs'],
 ['Conversational exploration','Follow-up questions, cited excerpts and no-evidence abstention'],
 ['Bonus web experience','Five-tab Streamlit interface, FastAPI and repeatable research harness']],widths=[172,354]),
 Spacer(1,13),P('WHAT THE EVIDENCE ACTUALLY SHOWS','eyebrow'),
 P('The original NewsBot midterm reported <b>96.18% BBC holdout accuracy</b> on 288 historical BBC articles. NewsBot 2.0 adds a distinct demo with <b>30 fictional articles</b>, <b>24 locally passing tests</b> and a controlled study of <b>24 synthetic queries</b>. The bilingual pivot attained <b>MRR@3 '+f"{probe['pivot_mrr']:.3f}"+'</b> versus <b>'+f"{probe['naive_mrr']:.3f}"+'</b> for the matched no-pivot baseline. These numbers are not 2026-news or production benchmarks.'),
 Image(str(ART/'retrieval_ablation.png'),width=495,height=180),
 P('Experimental comparison on an authored corpus; some probes selected after viewing data. No claims of independent validation.','small'),
 P('COMMERCIAL / ACADEMIC VALUE','h1'),
 P('The architecture demonstrates software engineering, classical NLP, optional modern multilingual embeddings, evaluation discipline and responsible AI safeguards. It is suited to a portfolio interview because an evaluator can inspect working source code, execute tests and trace results to the exact corpus rather than relying on screenshots or inflated performance claims.'),
 P('IMPLEMENTATION CHARACTERISTICS','h1'),
 bullet('Offline core with no paid API key or mandatory GPU; optional pretrained models are documented honestly.'),
 bullet('Document provenance, stable article IDs and SHA-256 hashes; explicit synthetic/real-source distinction.'),
 bullet('Streamlit frontend, FastAPI backend and command-line interface built over one reusable engine.'),
 bullet('Safe fallback behavior for absent translation packs, language models and weak retrieval evidence.'),
 bullet('24 locally passing tests and a research manifest recording corpus, per-query ranks and CV diagnostics.'),
 P('WHAT REMAINS BEFORE REAL DEPLOYMENT','h1'),
 P('A newsroom release would still need licensed multi-publisher data, external multilingual evaluation, independently rated summarization and answer support, accuracy and calibration testing on new sources, authentication, monitoring and human editorial acceptance. The frontend has not been independently browser-tested or deployed to a public URL in the current environment.'),

 P('Submission: José Miguel Tuozzo Izaguirre · Provisional group: JoseGroup · ITAI 2373','small'),
 P('GitHub base: https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System','small'),
 P('Instructor review pending; use the detailed Canvas final-project rubric to confirm any additional requirements.','small')]
p2=create(EXEC,exec_story)

reflection=[Spacer(1,42),P('PERSONAL REVIEW DRAFT  /  TEAM REFLECTIVE JOURNAL','eyebrow'),
P('NewsBot Intelligence 2.0<br/>Reflective Journal','cover'),
P('JoseGroup (provisional) · ITAI 2373','subtitle'),
HRFlowable(width='100%',thickness=3,color=TEAL),Spacer(1,18),
P('<b>Student currently identified:</b> José Miguel Tuozzo Izaguirre. The prior midterm repository describes a solo submission. Confirm with your instructor whether a solo final is permitted; do not invent collaborators. This document is a structured draft, not a personal testimony the student has already verified.','body'),
P('1 / What changed from the midterm?','h1'),
P('The midterm established a classical NLP workflow on historical BBC articles. The capstone organizes NLP into reusable services: analysis, multilingual retrieval, evidence-grounded interaction, import validation, API endpoints, web interface and evaluation. Its main conceptual advance is that a useful system must communicate provenance and uncertainty, not only return predictions.'),
P('2 / Technical lessons to discuss in your own words','h1'),
P('Explain why the new system separates model classification scores from retrieval similarity. Describe how exact source excerpts and citations reduce unsupported generation. Discuss how finite multilingual keyword equivalents differ from pretrained multilingual embeddings, and why optional language models must not be represented as having run unless they actually did.'),
P('3 / Challenges revealed by tests','h1'),
P('Local regression tests identified a NumPy/scikit-learn compatibility issue while normalizing a sparse-matrix centroid; the code was corrected and retested. The revised library passed 23 local regression and API tests. Controlled CV on 30 fictional examples yielded macro-F1 '+f"{metrics['macro_f1']:.4f}"+', showing that the tiny synthetic dataset is not suitable as a credible production accuracy sample.'),
P('4 / Personal contribution and AI-assistance disclosure','h1'),
P('<b>Complete personally before submission:</b> Which prior midterm elements did you originally implement? Which files did you review, execute, adjust or troubleshoot during the final? What did you learn through those actions? Describe all AI tool assistance according to course policy. Identify actual teammate names and completed contributions, or obtain instructor approval for individual work.'),
P('5 / Ethical and future-development reflection','h1'),
P('A robust next iteration would use licensed current articles, publisher/time-separated validation, human annotation for answer faithfulness, and clear user access policies. Source citation alone does not guarantee truth. Future work should evaluate fairness, translation quality and category drift before any high-stakes newsroom use.'),
Spacer(1,10),P('ACTION REQUIRED BEFORE SUBMISSION','eyebrow'),
P('Review or rewrite this journal so it genuinely reflects your work, challenges, learning and team participation. Confirm whether the group name is officially “JoseGroup”; replace it if necessary. Do not submit an unverified first-person claim.','small')]
p3=create(REFL,reflection)
print('Created:')
for x in (p1,p2,p3):
 from pypdf import PdfReader
 print(x.name,x.stat().st_size,'bytes',len(PdfReader(str(x)).pages),'pages')
