#!/usr/bin/env python3
"""Generate a two-page reflection draft grounded in verified NewsBot work.

Personal observations must be verified by the named student before submission.
The generator uses no invented experiments or collaborators.
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
styles.add(ParagraphStyle(name='TopSolo',fontName=BOLD,fontSize=17,leading=21,spaceAfter=7,textColor=NAVY))
styles.add(ParagraphStyle(name='SecondSolo',fontName=BOLD,fontSize=15,leading=19,spaceAfter=7,textColor=NAVY))
styles.add(ParagraphStyle(name='MetaSolo',fontName=FONT,fontSize=8.4,leading=12.3,spaceAfter=5,textColor=GRAY))
styles.add(ParagraphStyle(name='NoteSolo',fontName=BOLD,fontSize=8.1,leading=12,spaceAfter=7,textColor=ACCENT))
styles.add(ParagraphStyle(name='HeadSolo',fontName=BOLD,fontSize=10.15,leading=13,spaceBefore=6.3,spaceAfter=3,textColor=NAVY,keepWithNext=True))
styles.add(ParagraphStyle(name='BodySolo',fontName=FONT,fontSize=8.45,leading=12.15,spaceAfter=4.7,alignment=TA_LEFT))
styles.add(ParagraphStyle(name='SmallSolo',fontName=FONT,fontSize=7.7,leading=10.5,spaceAfter=4,textColor=GRAY))
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
    if actual is None:
        raise RuntimeError('Real-data results must be verified before generating the reflection.')
    doc=SimpleDocTemplate(str(DEST),pagesize=letter,leftMargin=51,rightMargin=51,topMargin=47,bottomMargin=58,
        title='What NewsBot Taught Me - Personal Reflection',author='José Miguel Tuozzo Izaguirre')
    blocks=[
        P('What NewsBot Taught Me','TopSolo'),
        P('Personal Reflective Journal | ITAI 2373 | October 2026','MetaSolo'),
        P('<b>Student:</b> José Miguel Tuozzo Izaguirre','MetaSolo'),
        H("1. Collaboration, planning, and ownership"),
        P("The most important shift in my thinking was learning to see NewsBot as one system instead of eight unrelated assignments. Each module has a purpose, but the value appears when the results support one another. A clean article becomes a reliable input for linguistic analysis; TF-IDF turns text into features; the classifier suggests a category; and sentiment and entities give a reader more context. Planning these connections taught me to ask what a result would mean to an editor before deciding what to calculate. I also learned that organizing work into small, inspectable stages makes problems easier to locate than trying to debug a large notebook all at once."),
        P("Because I am presenting the project under my own name, I need to be able to explain the design and defend the findings rather than rely on a checklist of completed cells. I have learned to use documentation, clear variable names, repeated tests, and the published execution record as ways to make technical work open to review. These habits matter whether I work independently or join a development team in the future."),
        H("2. Technical integration: what clean text really means"),
        P("Preprocessing taught me that removing more text is not always an improvement. URLs, HTML fragments, missing fields and duplicate articles can distort an analysis, yet capital letters, dates, numbers and the original wording still matter to named-entity recognition and dependency parsing. I therefore see the value of keeping different representations of an article for different tasks, rather than forcing every module to use one aggressively cleaned string. Tokenization, stop words and lemmatization help organize vocabulary; spaCy's POS and dependency labels offer another view of sentence structure, but neither should be mistaken for perfect understanding."),
        P("The strongest methodological lesson was about <b>data leakage</b>. A model can look impressive for the wrong reason if the vocabulary is learned from articles that later appear in the test set. In NewsBot, predictive TF-IDF belongs inside the training folds, while the final holdout stays separate. Comparing a dummy baseline, Naive Bayes, Logistic Regression and Linear SVM then becomes a meaningful experiment rather than simply choosing whichever score looks best. Working within Colab-style computing limits also showed me why shared spaCy processing, sparse features and controlled text lengths are practical design decisions."),
        H("3. Business value and the meaning of a good result"),
        P("The recorded BBC experiment retained <b>1,440</b> articles after removing exact duplicates. Its Linear SVM classified <b>277 of 288</b> held-out articles correctly: <b>96.18% accuracy</b> and <b>0.9605 macro-F1</b>. Those numbers are satisfying, but the confusion matrix changed how I interpret success. Eleven articles were still assigned to the wrong category, and entertainment had the weakest class F1, approximately <b>0.9515</b>. I learned to look for the cases behind the average, because an editorial team would experience the individual routing mistakes rather than an abstract percentage."),
        P("The other modules taught me similar caution. VADER captures word-level tone, not factual truth or the writer's opinion. An entity pair appearing together in a story is not proof of a relationship, and names such as 'Blair' and 'Tony Blair' can represent the same person under different forms. NewsBot can assist article triage and media research, but it should support decisions that people can check, not replace editorial judgment."),
        PageBreak(),
        P('Learning Beyond the Model','SecondSolo'),
        P('NewsBot Intelligence System | Reflection continued','MetaSolo'),
        H("4. Integration, debugging, and accountability"),
        P("Putting the modules together helped me recognize the difference between a convincing demonstration and a trustworthy evaluation. The fictional technology, football and politics articles show how the full pipeline responds to new text. They do not prove accuracy. That requires labeled articles held out from training, per-category scores, error analysis and a reproducible record of the run. I also learned why passing software tests is not the same as measuring a model: tests can confirm that code paths work, while held-out evaluation asks whether the predictions are actually useful."),
        P("Reviewing the GitHub Actions evidence added another lesson. An execution can successfully process the BBC data and still have trouble publishing files if the repository changes during the run. Seeing an error annotation alongside an overall green status showed me that I should read individual step logs, not rely on a badge alone. The resulting workflow, figures, model artifact and report make the results easier for another person to inspect. For me, good documentation is part of the engineering work, not something added only at the end."),
        H("5. What I would improve next"),
        P("My next experiment would use newer, appropriately licensed articles from several publishers. The BBC material comes from 2004-2005, so even strong results on its own holdout cannot show how NewsBot handles today's vocabulary, changing events or different editorial styles. I would compare macro-F1 and category-specific recall across sources, inspect incorrect predictions, and build a human-review option for ambiguous stories. I would also test whether confidence calibration helps decide when the system should abstain rather than force a category."),
        P("For information extraction, I would work on resolving entity aliases and evaluating recognition mistakes. For sentiment, I would compare VADER with methods that better handle quotations, context and irony. I would prioritize changes supported by measurable errors rather than adding features simply to make the project look more complex."),
        H("6. Professional growth and what I take forward"),
        P("NewsBot changed how I think about an AI project being 'finished.' A notebook that runs is a starting point; a credible project explains where the data came from, why a model was selected, what its mistakes look like, and whether another person can reproduce the result. I have gained a clearer understanding of how preprocessing, vectorization, grammatical analysis, sentiment, classification and NER complement one another, and why each output needs careful interpretation. Just as importantly, I am learning to communicate those details without exaggerating what the model knows."),
        P("Preparing this project for GitHub and a short video also pushed me to think about my audience. A professor or future employer should be able to find the code, follow the methodology and see the evidence without guessing where the results are. AI-assisted tools can help explain syntax and debug implementation issues, but I remain responsible for checking the outputs, understanding the choices and making my reflection genuinely my own. The lesson I want to carry forward is that technical ambition matters most when it is matched by transparency, patience, and a willingness to investigate mistakes."),
        P('Before submission: verify that the personal observations above reflect your own experience, and confirm the instructor\'s required dataset and project-submission approvals.','SmallSolo'),
    ]
    doc.build(blocks,onFirstPage=foot,onLaterPages=foot)
    print(DEST)
if __name__=='__main__':main()
