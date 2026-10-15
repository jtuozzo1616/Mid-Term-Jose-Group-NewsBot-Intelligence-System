# NewsBot — six-minute video demonstration
**ITAI 2373 | José Miguel Tuozzo Izaguirre**

This is a recording outline, not evidence of an uploaded video. Record actual screen content and speak naturally rather than reading each line without looking at the project.

**Before recording:** Open the [public project](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System), the [successful complete run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38491913062) and the charts in [outputs/](../outputs/). For the integrated examples, use the executed notebook from the run artifact or execute the `new_articles` cell in Colab first. Do not claim predictions that are not visible in the recording. **Use the numbers from the particular notebook being shown** if they differ from those below.

## 0:00–0:30 | Introduction
**Show:** Repository title and the README.

> Hello, my name is José Miguel Tuozzo Izaguirre. This is NewsBot Intelligence System for ITAI 2373. It uses eight natural language processing modules to explore historical BBC articles and help illustrate how editorial teams might organize and review news.

## 0:30–1:05 | Module 1: Data acquisition and context
**Show:** [01_data_distribution.png](../outputs/01_data_distribution.png), with the five news categories.

> Module One covers the dataset and the business problem. The labeled BBC training file includes business, entertainment, politics, sport and technology. After removing duplicate texts, 1,440 articles remain. This gives us a real dataset for studying topic classification, rather than relying on a few hand-written examples.

## 1:05–1:38 | Module 2: Preprocessing
**Show:** The notebook section `Module 2 — Preprocessing`; point to `normalize_text` and its test examples.

> Module Two prepares text for analysis. The code handles HTML fragments, web links, email addresses and inconsistent spacing. I also keep the original text available for grammar and entity recognition, because excessive cleaning can remove information those methods need.

## 1:38–2:13 | Module 3: TF-IDF
**Show:** [02_tfidf_category_terms.png](../outputs/02_tfidf_category_terms.png).

> Module Three uses TF-IDF to identify terms that distinguish different news topics. For example, business articles often discuss shares and markets, while technology stories mention software and users. The predictive TF-IDF features are fitted inside the training pipeline to avoid leaking information from the test set.

## 2:13–2:43 | Module 4: Part-of-speech tagging
**Show:** [03_linguistic_sentiment.png](../outputs/03_linguistic_sentiment.png); indicate the POS chart.

> Module Four uses spaCy to identify nouns, proper nouns, verbs and other grammatical categories. Comparing their proportions gives another view of how writing differs across news topics.

## 2:43–3:12 | Module 5: Syntax and semantics
**Show:** The `Module 5 — Syntax and semantics` section and its subject–verb–object extraction function.

> Module Five examines dependency structures to estimate who performs an action and what that action affects. The subject–verb–object patterns are helpful but approximate; complex or passive sentences may not be captured correctly.

## 3:12–3:43 | Module 6: Sentiment and emotion
**Show:** The sentiment panel in [03_linguistic_sentiment.png](../outputs/03_linguistic_sentiment.png).

> Module Six applies VADER to describe positive, negative and neutral lexical tone. It also counts selected emotion-related words. These outputs can describe language patterns, but they do not tell us whether a news report is true or whether a journalist endorses a quotation.

## 3:43–4:35 | Module 7: Classification and evaluation
**Show:** [05_model_cv_comparison.png](../outputs/05_model_cv_comparison.png), then [06_confusion_matrix.png](../outputs/06_confusion_matrix.png).

> Module Seven compares a dummy baseline, Naive Bayes, Logistic Regression and Linear SVM. On the verified GitHub run, tuned Linear SVM reached a training cross-validation macro-F1 of 0.9801. The independent set of 288 test articles had 277 correct predictions, or 96.18 percent accuracy, and a macro-F1 of 0.9605. The confusion matrix reveals the 11 mistakes, which matter more than simply reporting a high score.

## 4:35–5:05 | Module 8: Named entity recognition
**Show:** [04_ner_analysis.png](../outputs/04_ner_analysis.png), then a brief view of [07_entity_comentions.png](../outputs/07_entity_comentions.png).

> Module Eight recognizes people, organizations, places, dates and monetary amounts. Co-mention counts help locate names appearing in the same article, although they do not prove that the people or organizations are directly connected.

## 5:05–5:37 | Integrated article demonstration
**Show:** `Final integration — NewsBotIntelligenceSystem` and the `new_articles` cell, **after running it**. Show at least a technology and a sport example and their actual visible outputs.

> Finally, NewsBot combines article classification, sentiment, grammar and entity extraction in a single inference pipeline. These technology and sports stories are fictional demonstration inputs. They show what the tool returns for new text; they are not part of the labeled BBC holdout test.

## 5:37–6:00 | Conclusion
**Show:** [Technical report](MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf), [README](../README.md) and repository URL.

> NewsBot demonstrates a practical way to combine NLP techniques for human-reviewed article routing. Its main limitation is the historical single-publisher dataset; performance on current news has not been validated. The GitHub project includes the code, methodology, figures, evaluation results and report. Thank you for watching.

## Recording checklist

- Record **your own** voice and screen; aim for six minutes and stay within the instructor's 5–7-minute window.
- Make the code, graph titles and numbers readable (720p minimum; 1080p preferred).
- **Do not run all cells on camera**; model training can take several minutes. Use prepared outputs and execute only the short inference demonstration if the session is ready.
- Do not mix metrics from different executions. The **canonical GitHub evidence** is 96.18% / 0.9605 / 277 correct; a separately executed Colab session may differ.
- Use an accessible public or unlisted video URL, then add it to the README. The video is not considered completed until a recording exists.
- Suggested filename: `MT_Video_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.mp4`.
