# Optional NewsBot video demonstration — six-minute factual script

**Status:** a recording plan only. **No video has been recorded, uploaded or awarded points.**  
**Student:** José Miguel Tuozzo Izaguirre  
**Canonical project:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System  
**Required portfolio folder:** https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm

**0:00–1:00 — Introduction.** Open the GitHub portfolio's `ITAI2373-NewsBot-Midterm` folder, identify the NewsBot goal (assisted historical-news categorization, sentiment and entity exploration), then show the main repository, all eight modules and evidence files. Describe the project as individually attributed, without inventing teammates.

**1:00–2:00 — Article 1, technology.** Paste a *new fictional* technology article into the integrated notebook or locally launched Streamlit app. Show the **actual** category prediction, the NER output and VADER sentiment. State that this is not a current factual news report.

**2:00–3:00 — Article 2, sport.** Analyze a different *new fictional* sports article with the same pipeline. Describe any unexpected label/entity error instead of pretending every demo works perfectly. Explain that SVM scores are uncalibrated relative margins, not trustworthy probabilities.

**3:00–4:00 — Modeling and feature analysis.** Show `outputs/02_tfidf_category_terms.png` and `outputs/05_model_cv_comparison.png`. Explain TF-IDF, training-fold-only fitting, four model families and the **0.9801** tuned five-fold training macro-F1. Compare to the **0.0769** dummy baseline (which is from the untuned comparison).

**4:00–5:00 — Evaluation and NLP insights.** Show `outputs/06_confusion_matrix.png`. State **288** holdout articles, **277 correct**, **96.18% accuracy**, **0.9605 macro-F1**, and 11 errors. The weakest class was **entertainment** (F1 0.9515). Show `03_linguistic_sentiment.png` or `04_ner_analysis.png`, and explain that the VADER scores measure lexical tone while entity co-mentions do not establish real-world relationships.

**5:00–6:00 — Business value and limits.** Suggest human-reviewed newsroom routing, explain historical single-publisher limitations and lack of validation on new news sources, show the Colab launch button and cite one genuine engineering choice you made personally. End at the public portfolio URL.

**Export checklist:** record actual screen and clear voice, 720p minimum, 5–7 minutes maximum, legible code, working public/unlisted video link. Use instructor file naming `MT_Video_Group_[Name/Number]_[Student_Full_Name]_ITAI2373` and insert the link in the GitHub README **only after the upload succeeds**. The instructor describes this as optional bonus credit, with presentation also appearing in the 100-point rubric; ask if unclear.
