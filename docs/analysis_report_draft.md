# NewsBot Intelligence System — technical analysis (draft to complete after execution)

**Student:** José Miguel Tuozzo Izaguirre  
**Sole contributor:** José Miguel Tuozzo Izaguirre (solo permission pending)  
**Individual portfolio:** [WORKING PUBLIC GITHUB URL]  
**Dataset approval:** [DATE / CONFIRMATION]

## Executive summary
NewsBot integrates eight NLP modules as an editorial and media-intelligence prototype. The historical BBC News Classification labeled file contains up to 1,490 training-sourced news articles in five topics. The business use case is human-reviewed routing, thematic analysis and entity-monitoring. **Actual runtime analysis metrics MUST be inserted after approval and Colab execution.**

## 1. Dataset and preparation
Describe measured rows retained, category counts, duplicate/empty removal, median word length, historical/monolingual limitations. Use `outputs/run_manifest.json` and notebook exploration logs.

## 2. TF-IDF category features
Record at least 2 **actual** distinctive n-gram examples per category, explain category-specific terms, possible newspaper publisher artifacts and comparative strengths.

## 3. POS and syntax
Use `outputs/03_linguistic_sentiment.png`. Compare at least two POS proportions and one SVO pattern. State heuristic parse limitations and the 3,500-character truncation for language features only.

## 4. Sentiment, emotion proxy and NER
Describe the observed category polarity ordering, at least two named-entity categories, concentration and co-mentions. Explicitly distinguish unvalidated lexicon proxies from gold emotion classification, and co-mentions from genuine relationships.

## 5. Predictive experimental design
80/20 stratified labeled split; 5-fold cross-validation restricted to train; sklearn Pipeline ensures each fold fits TF-IDF only on the proper training subset. Compare Dummy, Multinomial Naive Bayes, Logistic Regression and Linear SVM. Tune best non-dummy class on training only by macro-F1.

## 6. Results (must be filled from actual run)
- Selected algorithm: [INSERT `selected_model` from `outputs/run_manifest.json`].
- Mean train-only CV macro-F1: [ACTUAL VALUE].
- Untouched holdout accuracy: [ACTUAL VALUE].
- Untouched holdout macro-F1: [ACTUAL VALUE].
- Strongest and weakest class: [ACTUAL CLASS F1 FROM `per_class_metrics.csv`].
- Frequent confusions: [ACTUAL MATRIX / EXCERPTS].
- Feature ablation: [ACTUAL TRAIN-CV UNIGRAM VS BIGRAM SCORES].

## 7. Business recommendations
Pilot **assisted** editorial category routing; track performance by category, reject/flag uncertain articles, audit language/model drift, periodically verify entity aliases and test externally with recent multi-source articles before deployment.

## 8. Limitation and responsible use
Historical source, no Health category, monolingual data, newspaper-classification imbalance, uncalibrated SVM scores, sentiment reporting vs article stance, named-entity errors, approximated SVO roles, no independent verification of recent material. The project is **not** a production readiness certificate.

## References
- BBC News Classification (Kaggle), https://www.kaggle.com/competitions/learn-ai-bbc/data
- Greene and Cunningham (2006), BBC text corpus citation, ICML.
- spaCy official documentation, https://spacy.io/usage/linguistic-features
- scikit-learn official documentation, https://scikit-learn.org/stable/modules/cross_validation.html
- NLTK VADER, https://www.nltk.org/api/nltk.sentiment.vader.html
