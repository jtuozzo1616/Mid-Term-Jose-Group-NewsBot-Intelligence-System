#!/usr/bin/env python3
"""Generate a data-grounded academic PDF after running the NewsBot notebook.

Run: python generate_final_report.py --group "Solo" --repo "https://github.com/USER/REPO"
The report refuses to manufacture empirical results if notebook outputs are absent.
"""
from pathlib import Path
import argparse, json, sys
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, KeepTogether, Table, TableStyle, PageBreak
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xml.sax.saxutils import escape

BASE=Path(__file__).resolve().parent
FNT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
if FNT.exists():
    pdfmetrics.registerFont(TTFont('NewsSans',str(FNT)))
    pdfmetrics.registerFont(TTFont('NewsSansBold',str(FNT.with_name('DejaVuSans-Bold.ttf'))))
    FONT='NewsSans';BOLD='NewsSansBold'
else:FONT='Helvetica';BOLD='Helvetica-Bold'
NAVY=colors.HexColor('#122B48');TEAL=colors.HexColor('#087C91');GRAY=colors.HexColor('#5B6474')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='HeadlineNB',fontName=BOLD,fontSize=21,leading=27,spaceAfter=13,textColor=NAVY))
styles.add(ParagraphStyle(name='HNB',fontName=BOLD,fontSize=11.5,leading=16,spaceBefore=13,spaceAfter=5,textColor=NAVY,keepWithNext=True))
styles.add(ParagraphStyle(name='Bnb',fontName=FONT,fontSize=9.2,leading=14.0,spaceAfter=7))
styles.add(ParagraphStyle(name='MetaNB',fontName=FONT,fontSize=8.6,leading=13,spaceAfter=5,textColor=GRAY))
styles.add(ParagraphStyle(name='NoteNB',fontName=BOLD,fontSize=8.2,leading=12,spaceAfter=8,textColor=TEAL))
styles.add(ParagraphStyle(name='CellNB',fontName=FONT,fontSize=8,leading=11))

def para(x,style='Bnb'):
    return Paragraph(str(x),styles[style])
def p(x):return para(x)
def h(x):return para(x,'HNB')
def safe(x):return escape(str(x))
def img(path,maxw=6.7*inch,maxh=4.25*inch):
    from PIL import Image as PIL
    with PIL.open(path) as im:width,height=im.size
    scale=min(maxw/width,maxh/height)
    return Image(str(path),width=width*scale,height=height*scale)
def footer(canv,doc):
    canv.saveState();canv.setStrokeColor(TEAL);canv.line(49,48,letter[0]-49,48)
    canv.setFillColor(GRAY);canv.setFont(FONT,7.5)
    canv.drawString(50,36,'ITAI 2373 | NewsBot Intelligence System | Methods, empirical evidence and limitations')
    canv.drawRightString(letter[0]-49,36,str(doc.page));canv.restoreState()

def create(argv=None):
    parser=argparse.ArgumentParser(description='Produce a report from verified notebook outputs.')
    parser.add_argument('--group',default='Solo')
    parser.add_argument('--repo',default='[VERIFIED PUBLIC REPOSITORY URL REQUIRED]')
    parser.add_argument('--members',default='')  # Backward-compatible legacy flag; solo submission ignores it.
    parser.add_argument('--output',default=None)
    args=parser.parse_args(argv)
    outs=BASE/'outputs'; docs=BASE/'docs';docs.mkdir(exist_ok=True)
    missing=['insights.json','run_manifest.json','per_class_metrics.csv','model_cv_comparison.csv','feature_ablation.csv','robustness_stress_test.csv','bootstrap_uncertainty.json']
    missing=[name for name in missing if not (outs/name).is_file()]
    verified=not missing
    if verified:
        try:
            from verify_release import verify
            verify(outs)
        except (AssertionError,ValueError,KeyError,FileNotFoundError) as exc:
            print('Empirical evidence incomplete:',exc)
            verified=False
    ins={};run={};classes=pd.DataFrame();cv=pd.DataFrame();ablation=pd.DataFrame()
    if verified:
        ins=json.loads((outs/'insights.json').read_text(encoding='utf-8'))
        run=json.loads((outs/'run_manifest.json').read_text(encoding='utf-8'))
        classes=pd.read_csv(outs/'per_class_metrics.csv')
        cv=pd.read_csv(outs/'model_cv_comparison.csv')
        ablation=pd.read_csv(outs/'feature_ablation.csv')
        required=['cv_macro_f1','holdout_accuracy','holdout_macro_f1','selected_model','rows']
        if not all(k in run for k in required):raise ValueError('Missing fields in run manifest. Rerun notebook.')
        if len(classes)<4 or classes.f1.isna().any():raise ValueError('Incomplete per-class results. Rerun notebook.')
        # Guard against accidentally using fixture runs as published evidence.
        if run['rows']<500 or run['rows']>2000:
            raise ValueError('Dataset size outside professor requirement; do not use fixture data.')
    output=Path(args.output) if args.output else docs/f'MT_Report_Group_{args.group.replace(" ","_")}_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf'
    output.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(output),pagesize=letter,leftMargin=53,rightMargin=53,topMargin=50,bottomMargin=65,
        title='NewsBot Intelligence System - ITAI 2373',author='José Miguel Tuozzo Izaguirre')
    st=[]
    repo_text=safe(args.repo)
    if str(args.repo).startswith(('https://github.com/','http://github.com/')) and '[' not in str(args.repo):
        repo_text='<link href="'+safe(args.repo)+'" color="#087C91">'+safe(args.repo)+'</link>'
    st.extend([para('NewsBot Intelligence System','HeadlineNB'),
      para('ITAI 2373 | NewsBot Midterm | Individual Technical Research Report','MetaNB'),
      para('Sole project contributor: José Miguel Tuozzo Izaguirre','MetaNB'),
      para('Submission designation: Individual / Solo | Date: October 2026','MetaNB'),
      para('Individual public GitHub repository: '+repo_text,'MetaNB')])
    if not verified:
        st.append(para('PRE-RUN DRAFT: NO REAL BBC EVALUATION RESULTS. Run the approved data in Colab and rerun this generator. Missing: '+safe(', '.join(missing)),'NoteNB'))
    else:
        st.append(para('GENERATED FROM EXECUTED NOTEBOOK OUTPUTS. Instructor approval is still needed for solo submission and the chosen Kaggle dataset; verify the repository URL.','NoteNB'))
    st.extend([h('Executive summary'),p('NewsBot is a small, interpretable, English-language newsroom-intelligence prototype, not an automated fact-checker. It combines eight NLP course modules in an end-to-end workflow: acquisition and business context, preprocessing, TF-IDF, POS patterns, syntactic relationships, sentiment and emotion proxies, supervised multi-class classification, and named entity recognition. It is designed to support human editorial routing, entity monitoring and cautious interpretation of historical article coverage.'),
        h('Business case and audience'),p('Editors need to triage articles quickly; media analysts need category-dependent terminology, sentiment context and named-entity summaries. Proposed operational metrics are topic-routing macro-F1, per-desk recall, review volume and frequency of entity extraction errors. The classifier does not validate whether reported statements are true. Manual review is essential for ambiguous predictions, names and consequential use cases.'),
        h('Dataset provenance and compliance'),p('The recommended source is Kaggle BBC News Classification, competition file <b>BBC News Train.csv</b>, with 1,490 labeled records before quality filtering (ArticleId, Text/Article, Category). Its five topical labels are <b>business, entertainment, politics, sport, tech</b>. It does not contain a Health label, despite that example appearing among the instructor’s illustrative system categories. The unlabeled competition test file must not be used to compute test metrics. The dataset consists of older 2004–2005 BBC reporting, so current-event or publisher-generalization claims are unsupported.'),
        p('Dataset URL: https://www.kaggle.com/competitions/learn-ai-bbc/data. The instructor requires approval before using any Kaggle dataset. Full copyrighted source articles and API credentials must not be placed in a public repository.'),
        h('Module 2 | Reproducible preprocessing'),p('The loader validates schema, nonempty text, labeled classes, article length and sample counts. It removes exact duplicate source articles before splitting. Unicode whitespace, simple HTML markup, escaped entities, URLs and email artifacts are normalized while preserving names and quantitative information for grammar, entity and sentiment analysis. A separate lemmatized lexical view supports interpretation without stripping features from raw text needed for NER and syntactic analysis.')])
    st.extend([h('Module 3 | TF-IDF weighting and feature inspection'),p('Descriptive corpus-level TF-IDF contrasts category mean weights with out-of-category mean weights for interpretable term charts. This exploratory analysis is explicitly separated from model evaluation: predictive vectorizers live inside scikit-learn Pipelines, so each cross-validation fold learns its vocabulary and IDF scores using training samples only. Parameters include feature cap, minimum and maximum document frequencies, sublinear term frequency and unigram/bigram alternatives.'),
        h('Module 4 | Part-of-speech patterns'),p('The spaCy small English pipeline labels grammatical tokens. NewsBot compares normalized document-level proportions of NOUN, PROPN, VERB, ADJ, ADV, ADP, NUM, PRON and AUX by category rather than raw totals, which would overcount longer documents. These comparisons are descriptive indicators of reporting style and topic, not causal descriptions of writing quality.'),
        h('Module 5 | Dependencies, syntax and semantic approximation'),p('Using spaCy dependency parses, the system records subject, object, noun chunk, sentence and passive structure counts. A limited rule extracts simple subject-verb-object tuples. These tuples are <b>heuristics</b>, not fully annotated semantic-role labels: they can miss passive voice, conjunctions, distant dependencies or implicit arguments. Linguistic annotations are capped at the first 3,500 characters per article for Google Colab Free CPU resource control; the classifier still receives full article text.'),
        h('Module 6 | Sentiment and emotion proxies'),p('NLTK VADER generates article-level continuous compound polarity and positive/neutral/negative labels using standard threshold values of ±0.05. An explanatory dictionary produces normalized lexical proxies for joy, fear, anger, sadness and surprise. The emotion proxies are <b>not</b> supervised or validated emotion classification, and polarity can reflect quotes or reported events rather than journalist approval. Comparisons aggregate the same metric by article category.'),
        h('Module 7 | Supervised classification experimental protocol'),p('After exact-text deduplication, the labeled corpus is stratified into 80% training and 20% untouched holdout, using random seed 42. A 5-fold stratified cross-validation experiment on the training subset compares Dummy majority, Multinomial Naive Bayes, Logistic Regression and LinearSVC with macro-F1 as the principal selection metric. GridSearchCV tunes only the best eligible non-dummy model using training folds, then the model is evaluated once on the holdout. Accuracy, macro- and weighted-F1, class-level precision/recall/F1, confusion matrix and error excerpts are exported for inspection.')])
    st.extend([h('Module 8 | Entity intelligence'),p('spaCy extracts PERSON, ORG, GPE, DATE and MONEY from original-case text. The notebook reports target entity counts per article by category, prominent names and illustrative same-article PERSON/ORG co-mention links. A co-mention means only that two names appeared in the same analyzed text; it does not imply contractual, financial, political or causal relationships.'),
        h('Integrated inference demonstration'),p('The reusable NewsBotIntelligenceSystem class accepts title and body, applies the fitted classification pipeline, returns a category and a clearly labeled score type, and adds VADER polarity, dictionary emotion proxy, POS rates, approximate SVO tuples and named entities. Newly authored fictional technology, sports and politics articles test data not present in the supervised training corpus. Empty input raises a validation error. SVM softmax-transformed margins are explicitly uncalibrated and are not trustworthy probability estimates.')])
    st.append(h('Measured results and error analysis'))
    if not verified:
        st.append(p('Real-data experimental results are <b>unavailable in this environment</b>. The labeled BBC CSV was not included in the uploaded files, and this isolated build environment cannot retrieve it or install the small trained spaCy pipeline. The notebook includes executable reporting code, but no score or finding should be quoted until the approved corpus is run end-to-end. Model quality cannot be inferred from synthetic smoke tests.'))
    else:
        st.append(p('Final holdout results calculated from the completed notebook: <b>'+safe(run['selected_model'])+'</b>; 5-fold tuned training CV macro-F1 <b>'+f'{run["cv_macro_f1"]:.4f}'+'</b>, untouched holdout accuracy <b>'+f'{run["holdout_accuracy"]:.4f}'+'</b>, untouched holdout macro-F1 <b>'+f'{run["holdout_macro_f1"]:.4f}'+'</b>, evaluated on '+str(run['rows'])+' labeled, cleaned documents. This is <b>within-corpus</b> evaluation only.'))
        table=[['Category','Precision','Recall','F1','Support']]
        for _,r in classes.iterrows():table.append([str(r.category),f'{r.precision:.3f}',f'{r.recall:.3f}',f'{r.f1:.3f}',str(int(r.support))])
        tt=Table([[para(c,'CellNB') for c in row] for row in table],colWidths=[112,80,80,75,70],hAlign='LEFT')
        tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dff0f3')),('BOTTOMPADDING',(0,0),(-1,0),9),('GRID',(0,0),(-1,-1),.25,colors.HexColor('#c8d4db')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,1),(-1,-1),5)]))
        st.append(tt)
        st.append(h('Baseline comparison and training-only feature ablation'))
        cvhead=[['Algorithm','CV macro-F1','CV accuracy']]
        for _,r in cv.iterrows():cvhead.append([safe(r['name']),f"{r['mean_cv_macro_f1']:.4f}",f"{r['mean_cv_accuracy']:.4f}"])
        cvtable=Table([[para(c,'CellNB') for c in row] for row in cvhead],colWidths=[180,110,110],hAlign='LEFT')
        cvtable.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dff0f3')),('GRID',(0,0),(-1,-1),.25,colors.HexColor('#c8d4db')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        st.append(cvtable)
        if len(ablation)>1:
            a=ablation.set_index('ngram_max')['cv_macro_f1'].to_dict()
            st.append(p('TRAIN-CV unigram macro-F1: '+f"{a.get(1,float('nan')):.4f}"+'; unigram+bigram macro-F1: '+f"{a.get(2,float('nan')):.4f}"+'. This comparison is descriptive about feature design and is not evaluated on the final holdout.'))
        st.append(p('Selected model parameters: '+safe(str(run.get('selected_parameters','not exported')))+'. Corpus source recorded as '+safe(run.get('dataset_origin','unknown'))+' with SHA-256 '+safe(run.get('source_file_sha256','?')[:16])+'… (full fingerprint in manifest).'))
        top=classes.sort_values('f1').iloc[0]
        st.append(p('The lowest-F1 category is <b>'+safe(top.category)+'</b> (F1 = '+f'{top.f1:.3f}'+'). This category is a priority for manual review and qualitative inspection of wrong predictions.'))
        for f in ['05_model_cv_comparison.png','06_confusion_matrix.png']:
            if (outs/f).is_file():st.extend([Spacer(1,9),img(outs/f,maxh=3.6*inch)])
    if verified:
        st.append(h('Research extension | Frozen-model robustness'))
        stress=ins.get('robustness_stress_test',[])
        if len(stress)==2:
            st.append(p('Unmodified holdout macro-F1 '+f"{stress[0]['macro_f1']:.4f}"+'; deterministic character-swap stress macro-F1 '+f"{stress[1]['macro_f1']:.4f}"+'. This measures sensitivity to synthetic typos, <b>not</b> robustness to current reporting or independent publishers.'))
        ci=ins.get('bootstrap_macro_f1_95pct_ci',[])
        if len(ci)==2:st.append(p('800-resample bootstrap 95% interval for historical holdout macro-F1: ['+f'{ci[0]:.4f}'+', '+f'{ci[1]:.4f}'+']. This interval ignores systematic publisher and time shift.'))
        if (outs/'08_robustness_stress_test.png').exists():st.append(img(outs/'08_robustness_stress_test.png',maxh=3.1*inch))
    st.append(h('Cross-module insights and business implications'))
    if verified:
        d=ins.get('sentiment',{}).get('mean_vader_by_category',{})
        if d:
            lows=sorted(d.items(),key=lambda x:x[1]);a,b=lows[0],lows[-1]
            st.append(p('VADER was lowest for <b>'+safe(a[0])+'</b> (mean '+f'{a[1]:.3f}'+') and highest for <b>'+safe(b[0])+'</b> (mean '+f'{b[1]:.3f}'+'). This describes polarity of one historical source, not journalist intent or population emotion.'))
        terms=ins.get('distinctive_tfidf_terms',{})
        if terms:
            snippets=['<b>'+safe(cat)+':</b> '+', '.join(safe(i['term']) for i in values[:3]) for cat,values in sorted(terms.items())]
            st.append(p('Category-distinctive TF-IDF expressions: '+'; '.join(snippets)+'. Distinctive expressions support editorial keyword audits but are not proof of outside-domain generalization.'))
        ner=ins.get('ner',{}).get('mentions_by_type',{})
        if ner:st.append(p('Entity mentions counted in annotated (length-capped) documents: '+', '.join(safe(k)+'='+str(v) for k,v in sorted(ner.items()))+'. The totals may be distorted by story length, truncation and NER mislabels.'))
        pos=ins.get('pos',{})
        if pos:
            cats=sorted(pos.get('PROPN',{}),key=pos['PROPN'].get)
            if len(cats)>1:st.append(p('Descriptive POS contrast: the proportion of proper-noun tags (PROPN) was lowest for <b>'+safe(cats[0])+'</b> ('+f"{pos['PROPN'][cats[0]]:.3f}"+') and highest for <b>'+safe(cats[-1])+'</b> ('+f"{pos['PROPN'][cats[-1]]:.3f}"+'). Linguistic annotations cover a limited text prefix and can be affected by source lowercasing.'))
        conf=ins.get('frequent_confusions',[])
        if conf:
            st.append(p('Most common holdout label confusion: actual <b>'+safe(conf[0]['actual'])+'</b> predicted <b>'+safe(conf[0]['predicted'])+'</b> ('+str(conf[0]['count'])+' examples). Inspect `error_analysis_excerpt.csv` for actual passages; routing to these desks needs human checks.'))
        else:
            st.append(p('There were no misclassified holdout examples recorded. This is not proof that predictions generalize to new publishers or current events.'))
        for figure,explanation in [('02_tfidf_category_terms.png','Distinctive historical category terms'),('03_linguistic_sentiment.png','POS and sentiment patterns by topic'),('04_ner_analysis.png','Named entity counts and frequency'),('07_entity_comentions.png','Illustrative co-mention graph; not factual links')]:
            if (outs/figure).exists():
                st.extend([Spacer(1,8),para(explanation,'MetaNB'),img(outs/figure,maxh=3.0*inch)])
    else:
        st.append(p('Once the notebook runs, compare category-specific lexical expressions against POS frequencies and entity mentions. Interpret at least three exact measured observations, quote the weakest class and typical confusion pairs, and explain operational consequences rather than converting small dataset correlations into claims about real-world trends.'))
    st.extend([h('Risks, next steps and responsible deployment'),p('This study uses single-source historical news and in-domain test splits. It does not establish robustness to 2026 articles, unseen publishers, healthcare news, multilingual input, implicit sentiment, factual truth or real-world decision thresholds. For a safer pilot: (1) require human review for unusual language or low relative model scores; (2) add external dataset evaluation; (3) check entity alias resolution; (4) monitor false categorization and distribution drift; (5) calibrate probabilities before using numeric review cutoffs; and (6) maintain versioned audit logs without unnecessarily storing personal data.'),
        h('Individual contribution and submission status'),p('José Miguel Tuozzo Izaguirre is the sole named project contributor. The package includes the notebook, reproducible software tests, documentation and a separate exactly two-page individual reflective journal. No teammates, team meetings, peer reviews or shared implementation work are claimed. <b>The original assignment specifies groups of 3–4; an individual submission requires the instructor’s explicit permission.</b> Publish the repository to GitHub and verify the URL publicly; course requirements concerning solo work and dataset choice are separate administrative conditions.'),
        h('References'),p('[1] BBC News Classification, Kaggle, https://www.kaggle.com/competitions/learn-ai-bbc/data. [2] Greene, D., and Cunningham, P., <i>Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering</i>, ICML (2006), source: https://github.com/derekgreene/bbc-datasets. [3] scikit-learn, <i>Common pitfalls and data leakage</i>: https://scikit-learn.org/stable/common_pitfalls.html. [4] spaCy linguistic features: https://spacy.io/usage/linguistic-features. [5] C. Hutto and E. Gilbert (2014), VADER, documentation: https://github.com/cjhutto/vaderSentiment. [6] Instructor ITAI 2373 Midterm assignment and starter notebook, October 2026.')])
    doc.build(st,onFirstPage=footer,onLaterPages=footer)
    print('Report:',output,'| real metrics included:',verified)
    return output
if __name__=='__main__':create()
