# NewsBot Intelligence System — ITAI 2373 Midterm

**Student:** José Miguel Tuozzo Izaguirre  
**Course:** ITAI 2373 — Natural Language Processing (Modules 1–8)  
**Canonical source:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System  
**Required portfolio folder:** [ITAI2373-NewsBot-Midterm](https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm)  
**Status:** All eight modules executed on labeled historical BBC articles; real results are published. **Dataset and individual-submission approvals are not documented as granted.**

> **Start here:** [Open the complete one-click Google Colab workflow](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/RUN_NEWSBOT_IN_COLAB.ipynb), or [open the full 36-cell analytical notebook](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/Midterm_NewsBot_Intelligence_System.ipynb).

## Verified experiment, not demo-fixture performance

The experiment uses the five-label **BBC News Classification** training file: business, entertainment, politics, sport, tech. The labeled file originally has 1,490 articles; the pipeline removes 50 identical-text duplicates and retains **1,440 substantive articles**, splitting them into **1,152 training** and **288 untouched holdout** articles. A public research mirror of the Kaggle competition CSV supplied the recorded run; its SHA-256 fingerprint is in [run_manifest.json](outputs/run_manifest.json). **Health is not a trained category.**

| Measurement | Recorded result |
|---|---:|
| Best model | Linear SVM, C = 2, TF-IDF 1–2 grams |
| Training-only tuned five-fold CV macro-F1 | **0.9801** |
| Untouched holdout accuracy | **96.18%** |
| Untouched holdout macro-F1 | **0.9605** |
| Incorrect holdout predictions | **11 of 288** |
| Strongest holdout F1 | sport, **0.9784** |
| Lowest holdout F1 | entertainment, **0.9515** |
| Bootstrap interval for holdout macro-F1 (800 resamples) | **[0.9334, 0.9800]** |

**Independent execution evidence:** [successful complete GitHub Actions run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38491913062) with software tests, eight-module notebook execution, real-artifact validation, report regeneration and downloadable executed notebook archive. [Run log and provenance](docs/RUN_STATUS.md), [research notes](docs/RESEARCH_EVIDENCE.md), [results interpretation](docs/Technical_Results_Summary.md). Local tests use synthetic fixtures only; they are **not** counted as historical BBC results.

## All eight required modules

| Module | Actual implementation |
|---|---|
| 1. Application context | Newsroom editorial routing use case, user needs, dataset audit |
| 2. Preprocessing | HTML/URL/email normalization, tokenization, stop words, lemmatization and edge cases |
| 3. TF-IDF | Category-discriminative terms; train-fold TF-IDF inside scikit-learn pipelines |
| 4. Part-of-speech | spaCy POS distribution and cross-category comparisons |
| 5. Syntax / semantics | Dependency analysis and explicitly heuristic subject–verb–object triples |
| 6. Sentiment / emotion | VADER sentiment; separately labeled exploratory word-list emotion proxy |
| 7. Multiclass classification | Dummy, Naive Bayes, logistic regression and linear SVM; tuning, CV, untouched holdout, confusion/errors |
| 8. NER | PERSON/ORG/GPE/DATE/MONEY extraction, category frequencies and article co-mentions |

The notebook includes an integrated engine for new, clearly labeled **fictional** demonstration articles, plus spelling-perturbation and bootstrap analyses. SVM relative margin displays are **not calibrated probabilities**. The source is from 2004–2005 and one publisher: these results do **not** establish performance on contemporary external news.

## Coursework deliverables — direct links

- [Complete notebook](Midterm_NewsBot_Intelligence_System.ipynb) and [one-click Colab launcher](RUN_NEWSBOT_IN_COLAB.ipynb).
- [Seven-page technical report PDF](docs/MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf), generated from measured data, with repository URL.
- [Exactly two-page reflective journal PDF](docs/NewsBot_Reflection_Solo.pdf) — **student review/personalization still needed**.
- [Eight experiment figures](outputs/), including category/TF-IDF, POS/sentiment, NER/co-mentions, CV, confusion matrix and robustness.
- [Per-class performance](outputs/per_class_metrics.csv), [CV comparison](outputs/model_cv_comparison.csv), [ablations](outputs/feature_ablation.csv), [full run manifest](outputs/run_manifest.json) and [saved trained pipeline](outputs/newsbot_classifier.joblib).
- [Academic quality audit](docs/FINAL_QUALITY_GATE.md), [current submission checklist](docs/Execution_and_Submission_Checklist.md), [contribution evidence](docs/Individual_Contributions.md), and [optional 6-minute demo script](docs/Video_Demo_6_Minute_Script.md).

The source code and evidence live in this repository. The **course-prescribed folder inside the student's personal portfolio** is linked above to avoid obscuring the portfolio submission path.

## Reproduce on free Google Colab

1. Open the [Colab launcher](RUN_NEWSBOT_IN_COLAB.ipynb) in Colab and select **Runtime → Run all**; it clones this repository, prepares packages and downloads the documented public research mirror unless you provide the instructor-approved official Kaggle CSV.
2. The runner executes all eight modules in a fresh kernel, checks the real-data output files, regenerates PDF reports and saves the fully executed notebook in a downloadable evidence ZIP.
3. Confirm the final pass indicator, `outputs/run_manifest.json`, all eight figures, the 288-article holdout evaluation, and the two PDFs. **Do not confuse the synthetic unit tests with model evaluation.**

For direct use after cloning:
```bash
python -m pip install -r requirements.txt nbclient nbformat reportlab pillow
python -m spacy download en_core_web_sm
python run_all_and_package.py --github "https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System"
python verify_release.py
```

The notebook needs network access for first-time dependencies and Kaggle/data access; the BBC articles themselves are intentionally omitted from this public repository. The exact original source and mirror are disclosed in [research provenance](docs/RESEARCH_EVIDENCE.md).

## Optional interactive dashboard and video

`dashboard.py` is a working Streamlit interface **source file**, not a hosted live site. The trained model artifact is published under `outputs/`. To start locally:

```bash
python -m pip install -r requirements-dashboard.txt
python -m spacy download en_core_web_sm
streamlit run dashboard.py
```

The rubric offers **up to +5 bonus points** for an interactive dashboard, subject to instructor assessment, and an optional 5–7 minute screen-recorded demonstration. A [narration/script guide](docs/Video_Demo_6_Minute_Script.md) exists; **no student video is claimed to be recorded or uploaded**.

## Submission integrity and remaining human-only requirements

This is a publicly accessible **individual project**, not a fabricated 3–4 person team. The professor's assignment formally specifies team collaboration and **pre-approval for a Kaggle dataset**. The project contains [a dataset approval request](docs/Dataset_Approval_Request.md) and [an individual-submission request](docs/Individual_Submission_Approval_Request.md); **requests are not evidence of approval**. Before submitting, personally check/complete the reflective journal, ensure your Canvas submission contains the correct portfolio link and required PDF, and resolve professor-controlled permission questions.

AI-assisted coding is permitted by the assignment as a learning aid, but system understanding, results interpretation and personal contribution statements must truthfully reflect the student's work. The PDF reports and software evidence are not substitutes for personal reflection or instructor decisions.

## Sources and responsible use

- [Kaggle BBC News Classification competition](https://www.kaggle.com/competitions/learn-ai-bbc/data)
- [Original BBC corpus research attribution](https://github.com/derekgreene/bbc-datasets)
- [scikit-learn](https://scikit-learn.org/stable/), [spaCy](https://spacy.io/), [NLTK/VADER](https://www.nltk.org/api/nltk.sentiment.vader.html)

Historical in-domain performance is not a production-readiness certificate, a fact checker, nor an automated editorial publishing system.
