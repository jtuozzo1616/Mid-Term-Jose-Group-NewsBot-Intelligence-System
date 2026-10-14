# Final 100-point rubric audit — evidence based (14 October 2026)

**Course:** ITAI 2373 — NewsBot Intelligence System
**Student:** José Miguel Tuozzo Izaguirre
**Live repo:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System
**Green real-data run:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38488603289
**Green artifact publication:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38489270753

| Rubric dimension | Maximum | Verified evidence | Remaining non-technical risk |
|---|---:|---|---|
| GitHub repository | 30 | Public standalone repo; 36 notebook cells; README, module code, 10 passing software tests, 8 BBC visualizations, CSV/JSON output and reproducibility manifest | Instructor specified a folder inside an individual portfolio; this is standalone per student's request |
| Technical implementation | 30 | All 8 NLP modules executed successfully; spaCy parsing/POS/NER, VADER, TF-IDF, 4 model families, clean stratified evaluation, 3 new fictional news inputs, packaged runner and optional Streamlit dashboard | No independent verification of behavior on other publishers or recent articles |
| Analysis and business insights | 30 | 1440 retained historical BBC articles, Linear SVM tuned CV macro-F1 0.9801, independent 288-item test accuracy 0.9618 and macro-F1 0.9605, confusion matrix, per-class metrics and entity/lexical/syntax insights, typo stress test and bootstrap uncertainty | Human must interpret findings and explain limitations; BBC historical accuracy is not real-world effectiveness |
| Presentation/documentation | 10 | Seven-page report grounded in measured results; exactly two-page personal reflection PDF; reproducible Colab launcher; video demonstration script and optional dashboard source | No student-recorded demo; journal needs firsthand personal review; group journal substituted by solo version |

## Source and data validity

- Training source: public research copy of the labeled BBC Kaggle competition training CSV; source SHA-256 recorded in outputs/run_manifest.json: f56a65dab2ea728505a639d2186a2b2f1c0939f28e8e89b5ed1c1fe9520b1323.
- The original 1,490-row file retained **1,440** articles after cleaning/duplicate removal; 1,152 were used for training and 288 held out for the final assessment. Five official categories: business, entertainment, politics, sport, tech (not health).
- 10 local synthetic-fixture tests passed and the complete data workflow completed on GitHub Actions. Synthetic-fixture evaluation must never be submitted as historical BBC performance.
- Class F1: business 0.9630, entertainment 0.9515, politics 0.9524, sport 0.9784, tech 0.9574.
- The two-page reflection discusses personal/project responsibility but requires the actual student to confirm what work they did and what they learned; no fictitious team meetings are claimed.
- The GitHub Actions evidence archive has the executed notebook, eight figures, CSVs, trained model, seven-page report and two-page reflection. Source news texts and error excerpts must not be published as public repository files.

## Remaining before final submission

1. Obtain professor acceptance of **solo instead of teams of 3–4**, of the **Kaggle dataset** and of the **standalone repository rather than an individual portfolio folder**, as required by the written rubric.
2. Personally review the 2-page journal; update it to describe your real decisions, obstacles and learning. Explicitly disclose AI assistance as required by your course.
3. Optionally record the requested 5–7 minute original screen/video demonstration if seeking bonus credit.
4. Submit the **public URL** and the exact **reflection PDF** in Canvas as the instructor directs.

This audit is evidence of implemented technical and presentation elements, **not a guarantee of a 100/100 grade**.
