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
    canv.drawString(49,32,'ITAI 2373 | NewsBot | Individual reflective journal | sole contributor')
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
        P('<b>Student:</b> José Miguel Tuozzo Izaguirre &nbsp;&nbsp; <b>Project arrangement:</b> Sole contributor','MetaSolo'),
        P('This is an individual adaptation of the required two-page group reflection. The assignment specifies teams of 3–4; instructor approval for an individual alternative is required. No team collaboration is claimed.','NoteSolo'),
        H('1. Collaboration and work organization'),
        P('Because this is a solo project, there are no group meetings, delegated responsibilities, peer code reviews or shared decisions to describe. Instead, the work is organized into the same eight NLP modules specified in the assignment, followed by one integration and evaluation stage. This creates a traceable sequence: prepare data; develop language analysis; train and compare classifiers; integrate predictions and insights; and verify the deliverables. The limitation is equally clear: without another teammate, cross-review and independent error detection must be replaced by explicit tests, readable documentation and instructor feedback.'),
        H('2. Technical integration challenges'),
        P('One important design problem is that different NLP operations need different representations of the same article. Token and lemma normalization help TF-IDF inspection, but entity recognition, syntax and sentiment benefit from original-case text. The design therefore keeps original and normalized views rather than applying aggressive cleanup everywhere. To prevent data leakage, the supervised TF-IDF vectorizer is fitted inside each training fold. Classification comparisons use training-only cross-validation, a tuned model and a separate holdout split.'),
        P(('Another challenge is reliability across data sources and runtime environments. The project checks for empty text, inconsistent column names, duplicates and missing labels. The actual historical BBC run analyzed <b>'+str(actual['rows'])+'</b> articles and achieved holdout macro-F1 <b>'+f"{actual['holdout_macro_f1']:.4f}"+'</b>, whereas synthetic regression tests merely exercise code paths. The results cannot establish modern-news performance.') if actual else 'Another challenge is reliability across data sources and runtime environments. The project checks for empty text, inconsistent column names, duplicates and missing labels. Local regression tests exercised the loader and model-training path using synthetic fixtures; these tests do <b>not</b> establish performance on BBC articles. Actual spaCy annotation, resource availability and full notebook execution remain to be checked in Google Colab with the licensed dataset.'),
        H('3. Business value and evidence limits'),
        P('NewsBot is designed for newsroom triage and media intelligence rather than automated fact-checking. Its five BBC topics are business, entertainment, politics, sport and tech. An editor could use a trained classifier to suggest routing while an analyst investigates characteristic terms, entity mentions and tone differences. However, the articles are older, belong to a single news source and do not justify claims about current trends or generalization to other publishers. Before reporting business impact, the actual holdout macro-F1, weakest class, typical classification errors and one measured entity or sentiment pattern must be recorded from the completed run.'),
        PageBreak(),
        P('Individual Contributions and Lessons','SecondSolo'),
        P('Student: José Miguel Tuozzo Izaguirre | ITAI 2373 | Individual submission','MetaSolo'),
        P('Measured BBC evaluation is incorporated below; the named student must still confirm firsthand observations and authorship.' if actual else 'Pre-run reflection draft: the named student must review the implementation, execute it and confirm the observations before submission.','NoteSolo'),
        H('4. Individual contribution and accountability'),
        P('This solo submission contains a prepared Colab notebook, implementation scaffolding for Modules 1–8, model comparison and validation procedures, output visualizations, an inference class, automated report-generation utilities and documentation. As the single submitter, I am responsible for understanding each module, running the approved dataset, explaining the pipeline accurately, correcting remaining errors, and recording my authentic observations. Any AI-assisted coding and drafting must be treated as learning support under the instructor’s academic-integrity policy—not as evidence of personal experiments that have not been performed.'),
        P(('The completed real-data metrics are documented in the execution manifest and the report, but a personally verified GitHub URL and my own review of the notebook remain required. The project distinguishes unit-test outcomes from holdout quality, and no fictional team meetings or co-authors are claimed.') if actual else 'The submission record still needs an independently verified public GitHub URL and real execution evidence. No teammates, peer reviews, meetings or results from unavailable news data are invented. The report distinguishes local software tests from supervised accuracy on actual BBC news.'),
        H('5. Future improvements'),
        P('The first priority after a successful Colab run should be <b>out-of-domain evaluation</b>: test on newer, legally reusable articles from more than one publisher and compare class-level recall and macro-F1 against the historical BBC holdout. This directly measures whether the model transfers to realistic editorial work. Later improvements could add calibrated class confidence, a human-review or abstention policy, entity alias resolution, duplicate-story clustering and more context-sensitive emotion methods. Each enhancement should be justified by an observed failure mode rather than added only to increase feature count.'),
        H('6. Professional development reflection'),
        P('The central learning opportunity is the difference between connecting library calls and producing a trustworthy analysis. A reproducible workflow must show exactly which transformations are used for description, which belong within cross-validation, and which data were withheld for final evaluation. POS, dependency parsing and NER can generate useful structured outputs, but heuristic labels and co-mentions should not be described as verified semantic relationships. Similarly, a high in-domain accuracy result would not by itself make NewsBot safe for production decisions.'),
        P('For a portfolio presentation, the responsible approach is to demonstrate the pipeline on unseen input, explain real errors and limitations, and show how those findings affect human review. My final personal reflection should add the specific debugging steps, measured findings and lessons confirmed during my own full notebook execution.'),
        H('Required confirmation before Canvas submission'),
        P('Obtain written permission for a solo alternative and the selected Kaggle dataset; complete the real-data run; replace preliminary language with firsthand findings; verify public GitHub access; and confirm that this individual reflection is accepted instead of a group journal.','SmallSolo'),
    ]
    doc.build(blocks,onFirstPage=foot,onLaterPages=foot)
    print(DEST)
if __name__=='__main__':main()
