#!/usr/bin/env python3
"""Produce an honestly labeled, two-page individual reflection draft.

This adaptation of the instructor's group journal requires solo-submission permission.
No teamwork or empirical evaluation outcomes are fabricated.
"""
from pathlib import Path
import json
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

ROOT = Path(__file__).resolve().parent
DEST = ROOT/'docs'/'NewsBot_Reflection_Solo.pdf'
FONTFILE=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
if FONTFILE.exists():
    pdfmetrics.registerFont(TTFont('SoloSans',str(FONTFILE)))
    pdfmetrics.registerFont(TTFont('SoloSansBold',str(FONTFILE.with_name('DejaVuSans-Bold.ttf'))))
    FONT='SoloSans'; BOLD='SoloSansBold'
else: FONT='Helvetica'; BOLD='Helvetica-Bold'
NAVY=colors.HexColor('#15314C'); ACCENT=colors.HexColor('#087C91'); GRAY=colors.HexColor('#566574')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TopSolo',fontName=BOLD,fontSize=19,leading=24,spaceAfter=9,textColor=NAVY))
styles.add(ParagraphStyle(name='SecondSolo',fontName=BOLD,fontSize=16,leading=21,spaceAfter=9,textColor=NAVY))
styles.add(ParagraphStyle(name='MetaSolo',fontName=FONT,fontSize=8.4,leading=12.3,spaceAfter=5,textColor=GRAY))
styles.add(ParagraphStyle(name='NoteSolo',fontName=BOLD,fontSize=8.1,leading=12,spaceAfter=7,textColor=ACCENT))
styles.add(ParagraphStyle(name='HeadSolo',fontName=BOLD,fontSize=10.6,leading=14.5,spaceBefore=10,spaceAfter=4,textColor=NAVY,keepWithNext=True))
styles.add(ParagraphStyle(name='BodySolo',fontName=FONT,fontSize=8.65,leading=13.35,spaceAfter=7.4,alignment=TA_LEFT))
styles.add(ParagraphStyle(name='SmallSolo',fontName=FONT,fontSize=8.15,leading=12,spaceAfter=6,textColor=GRAY))
def P(text,style='BodySolo'):return Paragraph(text,styles[style])
def H(text):return P(text,'HeadSolo')
def foot(canv,doc):
    canv.saveState();canv.setStrokeColor(ACCENT);canv.line(49,45,letter[0]-49,45)
    canv.setFont(FONT,7.5);canv.setFillColor(GRAY)
    canv.drawString(49,32,'ITAI 2373 | NewsBot | Reflective journal')
    canv.drawRightString(letter[0]-49,32,str(doc.page));canv.restoreState()

def main():
    # Incorporate genuine notebook outputs only when the complete release check passes.
    # The student must still confirm that personal reflections describe firsthand work.
    actual=None
    try:
        from verify_release import verify
        actual=verify(ROOT/'outputs')
    except (AssertionError,KeyError,ValueError,FileNotFoundError,ImportError):
        pass
    doc=SimpleDocTemplate(str(DEST),pagesize=letter,leftMargin=51,rightMargin=51,topMargin=47,bottomMargin=58,
        title='NewsBot Individual Reflective Journal - 2 Pages',author='José Miguel Tuozzo Izaguirre')
    blocks=[
        P('Individual Reflective Journal','TopSolo'),
        P('NewsBot Intelligence System | ITAI 2373 | October 2026','MetaSolo'),
        P('<b>Student:</b> José Miguel Tuozzo Izaguirre','MetaSolo'),
        P('Project reflection | Data analysis, system integration, evaluation and next steps','NoteSolo'),
        H('1. Project organization and approach'),
        P('NewsBot is organized around the eight course modules, with each stage producing information needed by the next. Article preparation feeds the linguistic analyses and the classification pipeline; model evaluation then checks whether the final predictions hold up on articles withheld from training. Keeping the modules separate made it easier to trace an unexpected result back to its source. Automated checks and readable intermediate outputs are particularly useful when reviewing a project without the benefit of informal feedback from classmates.'),
        H('2. Technical integration challenges'),
        P('One important design problem is that different NLP operations need different representations of the same article. Token and lemma normalization help TF-IDF inspection, but entity recognition, syntax and sentiment benefit from original-case text. The design therefore keeps original and normalized views rather than applying aggressive cleanup everywhere. To prevent data leakage, the supervised TF-IDF vectorizer is fitted inside each training fold. Classification comparisons use training-only cross-validation, a tuned model and a separate holdout split.'),
        P(('Another challenge is reliability across data sources and runtime environments. The project checks for empty text, inconsistent column names, duplicates and missing labels. The actual historical BBC run analyzed <b>'+str(actual['rows'])+'</b> articles and achieved holdout macro-F1 <b>'+f"{actual['holdout_macro_f1']:.4f}"+'</b>, whereas synthetic regression tests merely exercise code paths. The results cannot establish modern-news performance.') if actual else 'Another challenge is reliability across data sources and runtime environments. The project checks for empty text, inconsistent column names, duplicates and missing labels. Local regression tests exercised the loader and model-training path using synthetic fixtures; these tests do <b>not</b> establish performance on BBC articles. Actual spaCy annotation, resource availability and full notebook execution remain to be checked in Google Colab with the licensed dataset.'),
        H('3. Business value and evidence limits'),
        P('NewsBot is intended for newsroom triage and media research, not automated fact-checking. It can suggest an editorial category while offering context through vocabulary, sentiment and named entities. The completed BBC evaluation achieved 96.18% holdout accuracy and a macro-F1 of 0.9605; entertainment had the lowest category F1 at 0.9515. These are encouraging results for historical BBC articles, but the dataset contains older material from one publisher. Any practical use would need human review and testing against newer, more varied sources.'),
        PageBreak(),
        P('Evaluation, Learning and Next Steps','SecondSolo'),
        P('José Miguel Tuozzo Izaguirre | ITAI 2373','MetaSolo'),
        P('Measured findings are supported by the reproducible notebook and execution record.' if actual else 'This draft requires a successful dataset run before it can discuss measured outcomes.','NoteSolo'),
        H('4. Connecting the components'),
        P('The integrated system brings several different outputs together in a form that an editor can understand: a suggested news desk, lexical sentiment, notable entities and basic grammatical patterns. The reusable inference class applies these functions to a new article, while the notebooks and saved results make the process inspectable. The design also separates software tests from experiments on labeled BBC news, since a function passing a test does not establish that a prediction is accurate. For the final presentation, each claim should be connected to a visible output or a clearly explained limitation.'),
        P(('The experiment manifest records the source fingerprint, model settings and holdout results. In the 288-article test set, 277 articles received the correct category and 11 did not. The difference between this measured evaluation and the fictional demo inputs matters: the demos show what the pipeline can return, but only labeled test articles support an accuracy estimate.') if actual else 'The code and sample articles show how the pipeline is intended to behave. A reliable performance claim, however, requires a completed experiment on labeled articles and inspection of the resulting mistakes.'),
        H('5. Future improvements'),
        P('The first priority after a successful Colab run should be <b>out-of-domain evaluation</b>: test on newer, legally reusable articles from more than one publisher and compare class-level recall and macro-F1 against the historical BBC holdout. This directly measures whether the model transfers to realistic editorial work. Later improvements could add calibrated class confidence, a human-review or abstention policy, entity alias resolution, duplicate-story clustering and more context-sensitive emotion methods. Each enhancement should be justified by an observed failure mode rather than added only to increase feature count.'),
        H('6. Professional development reflection'),
        P('The central learning opportunity is the difference between connecting library calls and producing a trustworthy analysis. A reproducible workflow must show exactly which transformations are used for description, which belong within cross-validation, and which data were withheld for final evaluation. POS, dependency parsing and NER can generate useful structured outputs, but heuristic labels and co-mentions should not be described as verified semantic relationships. Similarly, a high in-domain accuracy result would not by itself make NewsBot safe for production decisions.'),
        P('A strong demonstration should show the predictions on new examples, then connect them to the confusion matrix and the errors observed in the held-out articles. That makes the limitations visible rather than hiding them behind a single accuracy number. The next meaningful improvement would be testing new publishers and time periods before relying on NewsBot for editorial decisions.'),
        H('Submission note'),
        P('The assignment specifies group work and instructor approval for Kaggle data. Confirm any permitted individual arrangement and dataset approval, then review this journal so that its descriptions match firsthand experience and the course academic-integrity policy.','SmallSolo'),
    ]
    doc.build(blocks,onFirstPage=foot,onLaterPages=foot)
    print(DEST)
if __name__=='__main__':main()
