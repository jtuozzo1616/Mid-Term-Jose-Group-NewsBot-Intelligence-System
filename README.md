# NewsBot Intelligence System
**ITAI 2373 — Natural Language Processing | Midterm Project**

**José Miguel Tuozzo Izaguirre**  
[Open in Google Colab](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/RUN_NEWSBOT_IN_COLAB.ipynb) · [Course portfolio](https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm) · [Verified execution](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38775732890)

NewsBot studies historical BBC news and brings eight natural language processing techniques into a single article-analysis pipeline. It sorts articles into editorial topics, examines language and sentiment, and extracts named entities. The intended use is to **assist** human editors and media researchers—not publish stories automatically or verify facts.

## Start here

| I want to… | Open |
|---|---|
| **Run the full project** | [One-click Google Colab notebook](RUN_NEWSBOT_IN_COLAB.ipynb) |
| **Review all eight modules** | [Clean, runnable notebook](Midterm_NewsBot_Intelligence_System.ipynb) |
| **See every executed cell and its results** | **[Completed notebook with outputs](docs/NewsBot_Executed_Results.ipynb)** — permanent, no artifact download needed |
| **Verify independent execution** | [Successful GitHub Actions run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38778575638) |
| **See the figures immediately** | [Eight charts and evaluation tables](outputs/) |
| **Read the research report** | [Technical PDF](docs/MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf) |
| **Read the personal reflection** | [Two-page PDF](docs/NewsBot_Reflection_Solo.pdf) · [First-person reading copy](docs/Personal_Reflection_Reading_Copy.md) |
| **Follow a short review route** | [Professor's review guide](docs/PROFESSOR_REVIEW_GUIDE.md) |
| **Explore the optional interface** | [Streamlit dashboard source](dashboard.py) |

Choose the [clean notebook](Midterm_NewsBot_Intelligence_System.ipynb) to run the project again, or the **[executed evidence notebook](docs/NewsBot_Executed_Results.ipynb)** to inspect all saved cell outputs immediately. Both are permanently available in this repository and mirrored in the [course portfolio](https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm).

## What the experiment found

The labeled BBC training file contains 1,490 articles from five categories: **business, entertainment, politics, sport and tech**. After removing 50 exact-text duplicates, the experiment used 1,440 articles: 1,152 for training and 288 for the final, untouched test set.

| Measure | Result |
|---|---:|
| Selected model | Linear SVM, TF-IDF unigrams + bigrams |
| Tuned five-fold training CV macro-F1 | **0.9801** |
| Holdout accuracy | **96.18%** — 277 of 288 articles |
| Holdout macro-F1 | **0.9605** |
| Most reliable class by test F1 | sport — 0.9784 |
| Class needing the most attention by test F1 | entertainment — 0.9515 |

The strongest signal is that a simple TF-IDF/SVM pipeline can organize articles effectively **within this historical BBC dataset**. Entertainment had the lowest F1, so it would be sensible to flag uncertain cross-category stories for editorial review rather than silently routing them.

[Confusion matrix](outputs/06_confusion_matrix.png) · [Model comparison](outputs/05_model_cv_comparison.png) · [Per-class evaluation](outputs/per_class_metrics.csv) · [Experiment manifest](outputs/run_manifest.json) · [Detailed findings](docs/Technical_Results_Summary.md)

These are results from a completed BBC-data run, not the synthetic articles used in software tests. The [execution record](docs/RUN_STATUS.md) explains the dataset origin, software versions and evidence.

## The eight NLP modules

| Module | Focus | Main evidence |
|---|---|---|
| **1. Data acquisition and business context** | Source, labels, cleaning and topic distribution | [Data distribution](outputs/01_data_distribution.png) |
| **2. Text preprocessing** | Normalize HTML, URLs and whitespace; preserve useful terms | [Notebook](Midterm_NewsBot_Intelligence_System.ipynb) |
| **3. TF-IDF** | Compare discriminative words across topics | [Term profiles](outputs/02_tfidf_category_terms.png) |
| **4. POS tagging** | Compare grammatical patterns using spaCy | [Linguistic patterns](outputs/03_linguistic_sentiment.png) |
| **5. Syntax and semantics** | Dependency parsing and approximate subject–verb–object patterns | [Notebook](Midterm_NewsBot_Intelligence_System.ipynb) |
| **6. Sentiment and emotion** | VADER polarity and a small illustrative emotion lexicon | [Sentiment analysis](outputs/03_linguistic_sentiment.png) |
| **7. Classification** | Compare four classifiers; tune and test the best model | [Models](outputs/05_model_cv_comparison.png) · [Confusion matrix](outputs/06_confusion_matrix.png) |
| **8. Named entity recognition** | Extract people, organizations, places, dates and money | [NER results](outputs/04_ner_analysis.png) |

The notebook also runs fictional technology, sports and politics articles through the integrated analysis class, and tests the trained classifier against light spelling perturbations. The demo articles are examples of system behavior, not labeled test evidence.

## Reproduce it

1. Open the [Colab launcher](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/RUN_NEWSBOT_IN_COLAB.ipynb) and select **Runtime → Run all**. It downloads this repository, installs dependencies and loads the historical BBC training data from the documented research mirror if a local CSV has not been supplied.
2. Allow time for spaCy parsing and model selection. The runner generates the eight charts, CSV/JSON metrics, PDFs and an executed notebook.
3. Read the final verification result and download the generated evidence archive. The original BBC article texts are **not** included in this public GitHub repository.

To run from a terminal after cloning:

```bash
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python run_all_and_package.py --github "https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System"
python verify_release.py
```

To try the optional Streamlit interface with the published model:

```bash
python -m pip install -r requirements-dashboard.txt
python -m spacy download en_core_web_sm
streamlit run dashboard.py
```

The dashboard is provided as runnable source code, not as a hosted website. Load the serialized model only from a source you trust.

## Interpretation and limits

BBC articles here are from **2004–2005** and represent one news publisher. Performance on present-day articles, other publishers or languages has not been measured. VADER describes lexical tone, not truth or the writer's views. Entity co-mentions do not establish real-world relationships, and SVM decision scores have not been calibrated as probabilities.

The [research notes](docs/RESEARCH_EVIDENCE.md), [technical summary](docs/Technical_Results_Summary.md) and [course review guide](docs/PROFESSOR_REVIEW_GUIDE.md) provide further methodology and limitations. The selected dataset originates from the [BBC News Classification Kaggle competition](https://www.kaggle.com/competitions/learn-ai-bbc/data); the source file is fingerprinted in the manifest.

**Course submission:** This repository lists José Miguel Tuozzo Izaguirre as the project student, and the course-named [portfolio folder](https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm) contains the assignment entry. The instructor's approval of the Kaggle dataset and individual submission arrangement has not been independently verified. The reflective journal should be checked against personal experience before submission. A video guide is [available here](docs/Video_Demo_6_Minute_Script.md); a recording link will be added when provided.
