# Review NewsBot in five minutes

**ITAI 2373 · José Miguel Tuozzo Izaguirre**

The [project homepage](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System) explains the approach; this page is a quick route to the evidence.

## 1 — Verify the system ran

**[Open the complete executed notebook with all outputs](NewsBot_Executed_Results.ipynb)**. Its 21 code cells were run on historical BBC data and include eight experiment figures, model evaluation, and three fictional demonstration articles. [The successful independent GitHub Actions run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38778575638) also verifies the execution, regression tests, and published results.

The [clean source notebook](../Midterm_NewsBot_Intelligence_System.ipynb) is available separately for rerunning the pipeline. The completed notebook is **committed to GitHub**, so reviewers do not need an expiring Actions artifact.

## 2 — Inspect the dataset and methodology

[Dataset distribution](../outputs/01_data_distribution.png) · [Source/provenance fingerprint](../outputs/run_manifest.json) · [Full notebook](../Midterm_NewsBot_Intelligence_System.ipynb)

The pipeline removes 50 duplicate articles from the 1,490-row labeled BBC file, retaining 1,440 records. Training uses 1,152 records; the independent, stratified holdout contains 288. All predictive TF-IDF fitting takes place within the training-side pipeline.

## 3 — Open the key figures

- [TF-IDF: words associated with each news topic](../outputs/02_tfidf_category_terms.png)
- [POS patterns and VADER sentiment](../outputs/03_linguistic_sentiment.png)
- [Named-entity frequencies](../outputs/04_ner_analysis.png) and [co-mentions](../outputs/07_entity_comentions.png)
- [Cross-validated model comparison](../outputs/05_model_cv_comparison.png)
- [Holdout confusion matrix](../outputs/06_confusion_matrix.png)
- [Light typo-stress experiment](../outputs/08_robustness_stress_test.png)

## 4 — Confirm the reported metrics

| Result | Verified BBC run |
|---|---:|
| Best model | TF-IDF + Linear SVM (C=2) |
| Training-only tuned five-fold macro-F1 | 0.9801 |
| Holdout accuracy | **96.18%** |
| Holdout macro-F1 | **0.9605** |
| Predictions | **277 correct / 11 incorrect out of 288** |
| Most difficult category (F1) | entertainment — 0.9515 |

[Per-class precision/recall/F1](../outputs/per_class_metrics.csv) · [Machine-readable metrics](../outputs/holdout_metrics.json) · [Scientific interpretation](Technical_Results_Summary.md)

## 5 — Review the written submission and video

[Technical report PDF](MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf) · [Two-page reflection PDF](NewsBot_Reflection_Solo.pdf) · [Video demonstration outline](Video_Demo_6_Minute_Script.md)

The video is not linked yet. The personal reflection needs final factual review by the student. Dataset-use and individual/group submission permissions are separate instructor decisions.

**Limitations:** These results are within the historical BBC corpus, not present-day multi-publisher validation. Sentiment is lexical polarity; NER and subject–verb–object parsing are approximate. The three fictional demonstration articles show an integrated pipeline, not an independent labeled benchmark.
