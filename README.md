# Mid-Term Jose Group: NewsBot Intelligence System

**ITAI 2373 — Natural Language Processing (Modules 1–8)**  
**Student:** José Miguel Tuozzo Izaguirre  
**Project source:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System  
**Verified status:** All 8 modules executed on historical labeled BBC news in [successful GitHub Actions run #38488603289](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38488603289); 10 synthetic-only software tests passed; aggregate results and updated PDFs are published.

### Quick access

| Goal | Open |
|---|---|
| **Run and download all evidence automatically (recommended)** | [Launch the one-click Colab notebook](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/RUN_NEWSBOT_IN_COLAB.ipynb) |
| Run the complete NLP notebook | [Open in Google Colab](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/Midterm_NewsBot_Intelligence_System.ipynb) |
| See the course-style 8-module notebook | [Midterm_NewsBot_Intelligence_System.ipynb](Midterm_NewsBot_Intelligence_System.ipynb) |
| One-click test on GitHub runners | [Verified BBC Evaluation workflow](.github/workflows/newsbot-verify.yml) — use Actions tab / Run workflow |
| Inspect research decisions | [Research and evidence notes](docs/RESEARCH_EVIDENCE.md) |
| Read the academic report | [Data-grounded PDF report (7 pages)](docs/MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf) |
| Read the exactly two-page solo reflection | [Empirical two-page reflection draft (personal review required)](docs/NewsBot_Reflection_Solo.pdf) |
| Explore the optional web interface code | [Streamlit dashboard](dashboard.py) (trained model now published in outputs; deploy Streamlit to open the web interface) |

## Verified historical BBC experiment — October 2026

**Actual held-out experiment**, not software-fixture scores. The recommended 1,490-row labeled source retained **1,440 articles** after validation/deduplication and was split into **1,152 training / 288 untouched testing** articles. With stratified training-only five-fold cross-validation and tuning, **Linear SVM** performed best.

| Measurement | Actual value |
|---|---:|
| Selected classifier | Linear SVM (C=2, TF-IDF ngrams=1–2) |
| Tuned five-fold training CV macro-F1 | 0.9801 |
| Independent holdout accuracy | **0.9618 (96.18%)** |
| Independent holdout macro-F1 | **0.9605** |
| Strongest holdout category | sport: F1 **0.9784** |
| Weakest holdout category | entertainment: F1 **0.9515** |

**Source and reproduction:** [run manifest](outputs/run_manifest.json) records the SHA-256 of the public mirror of the original Kaggle BBC training file, Python/library versions, train/holdout counts, model and selected hyperparameters. [Per-class metrics](outputs/per_class_metrics.csv), [CV comparison](outputs/model_cv_comparison.csv), [confusion matrix](outputs/06_confusion_matrix.png), [eight visualizations](outputs), [real-data evidence archive](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38488603289) and a [successful publication run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38489270753) are available.

**Business interpretation:** high *in-domain historical BBC* F1 supports a **human-reviewed routing prototype**, not fully automated publication. Entertainment has the lowest per-class F1 and deserves extra editorial scrutiny. Sport has perfect holdout recall in this sample, but that does not imply perfect performance on new publishers or recent news. Sentiment is lexical polarity rather than the journalist's beliefs; same-article entity co-mentions are not factual relationships.

**Run the optional dashboard locally** after cloning this repo:

```bash
python -m pip install -r requirements-dashboard.txt
python -m spacy download en_core_web_sm
streamlit run dashboard.py
```

The trained model is available at [outputs/newsbot_classifier.joblib](outputs/newsbot_classifier.joblib) and should be loaded **only when you trust this repository**, because Python joblib/pickle formats are not safe for untrusted files. GitHub itself shows source code and PDFs; a live Streamlit website requires separate deployment. The course's optional demo video must be recorded by the student.

## What NewsBot does

This end-to-end, English-language **historical BBC news** NLP system loads labeled articles, cleans text, identifies discriminative TF-IDF features, compares part-of-speech usage, extracts dependency-based syntax heuristics, measures VADER lexical sentiment and an explicitly limited emotion proxy, evaluates several multi-class topic classifiers, and maps named-entity co-mentions. A final engine processes original fictional demonstration articles end to end.

**Labels:** business, entertainment, politics, sport, tech. **Health is not included** in the recommended BBC dataset, so the model must not pretend it can classify it. The tool is an **editorial triage prototype**, not a fact checker.

## Execute and verify

### Google Colab (free CPU)

1. Click **Open in Google Colab** above and select *Runtime → Run all*.
2. The notebook installs its dependencies and English spaCy small model, then downloads the public research mirror of the recommended Kaggle **BBC News Train.csv** unless a user-supplied official CSV is present. If automatic download fails, obtain the CSV from the [original Kaggle competition](https://www.kaggle.com/competitions/learn-ai-bbc/data), review terms and upload it.
3. Let all notebook cells finish. Check five labels, data quality counts, cross-validation macro-F1 and **independent held-out** results. Download outputs before the temporary Colab session expires.
4. For the full PDF + evidence ZIP, run `python run_all_and_package.py --github https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System` in a prepared project directory (the [one-click Colab launcher](RUN_NEWSBOT_IN_COLAB.ipynb) clones this repository and automates installation, execution and downloading the evidence ZIP (no additional project ZIP upload)).

### GitHub Actions (automated, no paid Colab)

Open **Actions → Verified BBC Evaluation → Run workflow**, or inspect the run triggered when the workflow was installed. The workflow installs the same dependencies, passes offline regression tests, runs the complete 8-module notebook on the labeled BBC source, verifies metrics and charts, and saves an evidence ZIP. When repository policy permits writing from actions, it also publishes **only** allowed aggregate metrics, figures, and regenerated report PDFs, **not the original BBC articles**. Do not treat red CI as evidence of success.

### Reproduction controls

- Dataset: BBC News Classification, historical articles. The competition training split normally has 1,490 labeled records, and there are only five labels.
- Strict 80/20 stratified held-out split; training-only 5-fold CV and hyperparameter search; Dummy, Naive Bayes, Logistic Regression, Linear SVC.
- No train/holdout vocabulary leakage: predictive TF-IDF fitted inside scikit-learn `Pipeline`/folds.
- Save real-model macro-F1, accuracy, classification report, per-class scores, confusion matrix, CV comparison, ablation, lexical/category charts, entity network, sensitivity perturbations, and a bootstrap interval.
- Synthetic fixtures in `tests/` are for software QA and must **never** be presented as BBC accuracy results.
- No Kaggle API key, BBC article CSV, or pickle from unknown sources is committed.

## Compliance and submission caveats

The assignment explicitly says **teams of 3–4**, **instructor approval of Kaggle data**, and an **ITAI2373-NewsBot-Midterm folder inside an individual portfolio**. This repository is standalone at the student's request, with solo work attributed to a single contributor. The code cannot waive those professor-controlled requirements. Confirm that this format and source are acceptable to avoid nontechnical rubric deductions. The optional 5–7 minute demo must be recorded and linked by the student if claiming bonus credit. The two-page reflective journal describes technical methodology but requires **personal verification and firsthand reflection** before submission.

## Structure

```text
Mid-Term-Jose-Group-NewsBot-Intelligence-System/
  Midterm_NewsBot_Intelligence_System.ipynb
  RUN_NEWSBOT_IN_COLAB.ipynb
  dashboard.py
  run_all_and_package.py
  verify_release.py
  generate_final_report.py
  reflection.py
  requirements.txt
  requirements-dashboard.txt
  .github/workflows/newsbot-verify.yml
  data/                 (CSV NOT committed)
  outputs/              (generated only after an authenticated data run)
  docs/                 (report, reflection, technical evidence)
  tests/                (synthetic-only software tests)
```

## Design and evaluation controls

| Control | Implementation |
|---|---|
| Labeled data | 1,490-row BBC competition training file (subject to cleaning and availability) |
| Data quality | Missing/empty texts; exact-text deduplication; category assertions; word counts |
| Holdout | 80% training / 20% untouched test, stratified, `random_state=42` |
| Model selection | Five-fold stratified **training-only** CV, macro-F1 |
| Models | Dummy, MultinomialNB, LogisticRegression, LinearSVC |
| Hyperparameters | GridSearchCV on training folds for top non-dummy model |
| Feature leakage protection | TF-IDF **inside sklearn Pipeline**; never fitted on held-out test set |
| Performance | Accuracy, macro/weighted F1, per-category precision/recall/F1, confusion matrix, errors |
| Linguistic analysis | spaCy original text, bounded to first 3,500 chars/article for speed |
| NER relationships | Same-article co-mentions only, no claim of causality |
| Sentiment | VADER full article, descriptive polarity, not objectivity measure |
| Emotions | Transparent dictionary *proxy*, **not** a trained/validated emotion classifier |
| Inference | Single trained pipeline reused, no fake padding vectors |
| Confidence | SVM margins are shown as **uncalibrated relative scores** |

## Expected output artifacts (only **after Run all**)

`outputs/01_data_distribution.png`, `02_tfidf_category_terms.png`, `03_linguistic_sentiment.png`, `04_ner_analysis.png`, `05_model_cv_comparison.png`, `06_confusion_matrix.png`, `07_entity_comentions.png`, `08_robustness_stress_test.png`, `model_cv_comparison.csv`, `per_class_metrics.csv`, `error_analysis_excerpt.csv`, `insights.json`, `run_manifest.json`, `newsbot_classifier.joblib`.

**No accuracy or macro-F1 number is claimed here prior to real-data execution.** The report and reflection should use numbers directly from `outputs/run_manifest.json` after an approved, successful run.

## Limitations and use policy

Historical single-publisher BBC corpus, not a multilingual/current feed; domain shift unmeasured; NER/semantics imperfect; emotion vocabulary not validated; sentiment can misread quotations or report controversial subjects; document length truncated *for linguistic analyses only*; no automated publication/decision authority. Do not claim this establishes factual truth, live trend monitoring, or perfect performance.

## Attribution and further reading

- BBC News Classification, Kaggle, https://www.kaggle.com/competitions/learn-ai-bbc/data (competition source and dataset usage rules).
- D. Greene and P. Cunningham (2006), *Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering*, ICML, original BBC corpus scholarly attribution.
- scikit-learn official documentation: https://scikit-learn.org/stable/modules/cross_validation.html , https://scikit-learn.org/stable/modules/feature_extraction.html
- spaCy documentation: https://spacy.io/usage/linguistic-features
- NLTK/VADER: https://www.nltk.org/api/nltk.sentiment.vader.html

The instructor's `Midterm_NewsBot_Intelligence_System_student.ipynb` provided the module-by-module starter scaffold.

## Optional +5 dashboard opportunity

The included `dashboard.py` can display actual outputs and analyze a pasted article. Run the notebook first, install `streamlit`, and execute `streamlit run dashboard.py` locally. Bonus credit is subject to instructor grading; a script alone does not demonstrate a deployed live dashboard.

## Verified-output report generation

After **Colab Run all** completes on the *instructor-approved* BBC training CSV, download the resulting `outputs/` folder into this project and run:

```bash
python -m pip install -r requirements.txt reportlab pillow
python generate_final_report.py --group "Solo" --repo "https://github.com/USERNAME/REPOSITORY"
```

This creates the required-naming technical report and includes real CV/holdout metrics, actual class precision/recall/F1, sentiment comparisons and actual exported figures. When output files are missing, the script labels the PDF **pre-run draft**, never fabricates results. Confirm your public repository URL before submitting. The separate two-page journal must contain firsthand individual reflections, not invented teamwork. See `QUICK_START_EN.md` and `docs/Submission_Audit_100_Point_Rubric.md`.

## Offline regression tests

Run `python -m unittest discover -s tests -p "test_*.py" -v` from the project folder. Five test cases currently pass on synthetic fixtures. Results from these fixtures have **no relationship to real BBC model performance** and are never copied into the deliverable outputs. Details: `docs/VERIFICATION_RESULTS.md`. The optional dashboard dependencies are in `requirements-dashboard.txt`.

## Streamlined end-to-end execution and automatic evidence package (new)

The notebook now looks for a local copy of `BBC News Train.csv`. If none exists, it attempts to download the public research mirror at https://github.com/alvinrach/learn-ai-bbc with a fully logged provenance. The underlying Kaggle competition and original BBC copyright remain the primary source context. Nothing redistributes the article texts through this repository. If the mirror is unavailable, download the official Kaggle labeled CSV and upload it normally.

After unpacking this repository in **Google Colab** with an internet-enabled runtime, use the following from the extracted project directory:

```bash
python -m pip install -r requirements.txt nbclient nbformat reportlab pillow
python -m spacy download en_core_web_sm
python run_all_and_package.py --github "https://github.com/YOUR_ACCOUNT/YOUR_REPO"
```

It executes the entire notebook in a fresh kernel, verifies the five-class real-data artifacts, regenerates the metrics-grounded report, and writes `NewsBot_VERIFIED_EXECUTION_EVIDENCE.zip`. The script fails rather than claiming a successful experiment if the corpus, spaCy model, or analysis output is missing. **You must replace the example GitHub address with a working, publicly viewable repository link.**

For your normal interactive Colab workflow, simply open `Midterm_NewsBot_Intelligence_System.ipynb` and select **Runtime → Run all**. If you already uploaded the whole project folder, run `python verify_release.py` and then `python generate_final_report.py --group Solo --repo YOUR_PUBLIC_URL` in the project folder.

Background references and implementation rationale: `docs/RESEARCH_EVIDENCE.md`; test and grading gap report: `docs/FINAL_QUALITY_GATE.md`.

## Evaluated research extension

After the model has already been selected and the final holdout evaluation made, NewsBot measures how deterministic light spelling corruption affects macro-F1 on the same historical labeled holdout. This is a **within-corpus stress test**, not evidence about modern news. It also reports an 800-replicate bootstrap interval for holdout macro-F1 to illustrate sampling uncertainty. Results are saved as `robustness_stress_test.csv`, `08_robustness_stress_test.png`, and `bootstrap_uncertainty.json`. The report imports these observations automatically only after execution.

## Simplest option — bundled Colab launcher

Open `RUN_NEWSBOT_IN_COLAB.ipynb` in Google Colab, execute the cells in order, and upload the full `NewsBot_ITAI2373_Improved_Complete_Package.zip` from the Files upload dialog. The launcher installs the free dependencies and trained English language model, executes the original notebook, fails if real outputs are missing, builds the evidence-grounded PDF and starts a ZIP download. For the final PDF's mandatory working GitHub link, replace `PUBLIC_GITHUB_URL` with the URL of your own published repository.