# Individual project contributions — repository evidence

**Student named in the project:** José Miguel Tuozzo Izaguirre  
**Course:** ITAI 2373  
**Public source:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System  
**Portfolio folder:** https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm

This repository is explicitly presented as an individual effort. No fictitious team members, meetings, peer reviews or task divisions are asserted. The class assignment's group-work expectation can only be waived by the instructor.

## Traceable implementation areas

| Area | Inspectable source | Real execution evidence |
|---|---|---|
| Data provenance, validation and preprocessing | Notebook Module 1–2 (cells 4–8) | `outputs/run_manifest.json`, `outputs/01_data_distribution.png` |
| Exploratory TF-IDF features | Notebook Module 3 (cells 9–10) | `outputs/02_tfidf_category_terms.png` |
| POS and dependency patterns | Notebook Modules 4–5 (cells 11–13, 17–18) | `outputs/03_linguistic_sentiment.png`, `outputs/insights.json` |
| VADER, lexical emotion proxy and entity extraction | Notebook Modules 6, 8 (cells 14–19) | `outputs/03_linguistic_sentiment.png`, `outputs/04_ner_analysis.png` |
| Four classifier families, CV, ablation, holdout | Notebook Module 7 (cells 20–25) | `outputs/model_cv_comparison.csv`, `outputs/holdout_metrics.json`, `outputs/per_class_metrics.csv` |
| Integrated article prediction, regression checks | Notebook cells 29–33; `tests/test_pipeline.py`; `dashboard.py` | [successful integration workflow](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38775732890) |
| Reports, interpretation and delivery | `generate_final_report.py`, `reflection.py`, `docs/Technical_Results_Summary.md` | Seven-page technical report and a two-page **personal-review-required** reflection |

**Technical verification:** 10 automated tests passed in CI; all eight NLP modules executed against the BBC labeled corpus. The published holdout accuracy is 96.18% and macro-F1 is 0.9605. Synthetic test data are never cited as real BBC evaluation.

**Personal authorship statement — finish only after first-hand review:** Explain what you actually built, tested, changed, understood, and learned; describe real difficulties and the role of any AI assistance honestly. Repository commits and generated documents establish files, not proof of any person's individual thought processes or group participation. Do not sign claims you cannot substantiate.
