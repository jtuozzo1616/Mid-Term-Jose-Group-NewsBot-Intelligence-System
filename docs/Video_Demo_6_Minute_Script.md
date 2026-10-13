# Optional 5–7 Minute Video Demonstration — Narration and Shot List

**Status:** Ready-to-customize script, not a recorded or uploaded video. Do not claim bonus points until the video is actually filmed and accepted.

**0:00–1:00 | Introduction and project overview**
Show your **actual public personal GitHub URL**, the `ITAI2373-NewsBot-Midterm` folder, README, notebook, figures, output manifest and collaboration record. Identify yourself as the sole contributor; do not invent team contributions. Introduce the problem: editor review of historical BBC news articles and topic-based intelligence.

**1:00–2:00 | Live unseen article #1 (Technology)**
Show an invented, clearly fictional original technology article in the notebook or optional Streamlit app. Run the code live, narrate category, top entities, and VADER sentiment. Explain why this is an unseen sample distinct from training records.

**2:00–3:00 | Live unseen article #2 (Sport)**
Repeat with an original fictional football article. If the model's prediction is wrong or NER incomplete, say so rather than silently choosing a replacement. Show the complete input → category → NER → sentiment flow and state that confidence for SVM margins is uncalibrated.

**3:00–4:00 | Technical deep dive**
Display generated `02_tfidf_category_terms.png` and `05_model_cv_comparison.png`. Give ONE concrete, real, numeric result: the selected algorithm's mean 5-fold *training* CV macro-F1 [VALUE]. Show how vectorization is fitted within pipeline CV rather than using the test set.

**4:00–5:00 | Evaluation and linguistic analysis**
Show `06_confusion_matrix.png` plus one category-specific actual error [TRUE → PREDICTION] and why it might happen. Show POS or NER plot from notebook. Explain historical BBC source bias and the interpretation limit for VADER emotion terms.

**5:00–6:00 | Business relevance, individual reflections and conclusion**
Explain how editors could route mixed-category articles to human review and why calibrated scores/newer publishers would be needed before production. Reflect on authentic engineering tradeoffs and individual development and testing. Show the README's repeatable Colab steps and end with verified repository URL.

**Export checklist:** 720p minimum, readable code, clear narration, public/unlisted YouTube/Vimeo URL with working access, target 6 minutes (5–7 permitted), filename convention `MT_Video_Group_[Name/Number]_[Student_Full_Name]_ITAI2373`, and URL in each individual repo README. Confirm with the professor whether the video is compulsory because the rubric and 'optional bonus' section are inconsistent.
