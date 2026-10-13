# NewsBot intelligence system — Research and evidence dossier

**ITAI 2373 | José Miguel Tuozzo Izaguirre | October 2026**

## 1. Provenance, data rights, and scope

The recommended Kaggle BBC News Classification competition dataset includes **1,490 labeled training records** and an unlabeled test set. `BBC News Train.csv` is the labeled input for this project, with article ID, text (`Article` on Kaggle or `Text` in some public mirrors), and one of five categories: **business, entertainment, politics, sport, tech**. We do not pretend Health is a sixth category; a sixth category would require a separate supervised labeled corpus and external evaluation. The competition page lists the material as subject to competition rules. The original BBC news corpus description credits Greene and Cunningham (2006), describes 2,225 articles dated **2004–2005**, and expressly reserves original article copyright to the BBC. Thus, repository artifacts exclude the article contents, and findings describe a historical single-publisher benchmark, not present-day news.

- Competition dataset, schema, size, terms: https://www.kaggle.com/competitions/learn-ai-bbc/data
- Original research corpus provenance and BBC copyright: https://github.com/derekgreene/bbc-datasets
- Primary academic attribution: D. Greene and P. Cunningham. *Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering*, ICML, 2006 (linked in original research repository).
- Clearly indicated optional public research mirror of the competition training CSV: https://github.com/alvinrach/learn-ai-bbc (not the official Kaggle distributor).

## 2. Methodological decisions and research justification

**Preprocessing.** Normalize HTML entity escaping, whitespace, email addresses, and URL strings. Preserve original capitalization and numbers in the spaCy analysis view because entity detection and syntactic patterns can depend on case and context. A separate token and lemma view demonstrates normalization but is not incorrectly used as an input to NER. Remove exact repeated texts *before* splitting to avoid blatant train/test contamination. Near duplicates and reporting on the same news event may remain, limiting independence.

**TF-IDF / feature selection.** TF-IDF weighs a term by its frequency in an article and its scarcity across articles. We compare category-level descriptive distinctive terms, but learn supervised vector vocabularies and inverse-document frequencies only inside each fold of the scikit-learn `Pipeline`. Otherwise test leakage would inflate accuracy. Compare both unigrams and (1,2)-grams; tune vector cap and model-specific regularization with inner training CV.

- Pipelines and leakage control: https://scikit-learn.org/stable/common_pitfalls.html
- Text representations: https://scikit-learn.org/stable/modules/feature_extraction.html

**POS, dependencies, and entity extraction.** Use `en_core_web_sm`, which includes a tagger, parser, lemmatizer and statistical named entity recognizer. Relative POS ratios are more comparable than raw token counts across documents of different length. Subject–verb–object triplets are extracted with syntactic dependency rules, not with a gold-standard trained semantic-role labeler. Entity co-mentions mean that two strings co-occur in the same article, not that they have an actual social, political, or business relationship. The first 3,500 characters are annotated to fit free-resource limits while supervised classification sees the complete text. Older BBC competition text is substantially lower-cased, making proper-name recognition potentially less reliable than on normally cased news.

- spaCy pipelines: https://spacy.io/usage/processing-pipelines
- POS/dependencies/entities: https://spacy.io/usage/linguistic-features

**Sentiment and lexical emotion proxies.** NLTK's VADER compound polarity is a lexicon-based indicator. Use the commonly documented ±0.05 boundaries for positive, negative and neutral, but refrain from equating polarity with objective fact, author stance, or ethical evaluation. A tiny transparent dictionary for fear, joy, anger, sadness and surprise supports an exploratory demo only; it does not constitute a scientifically validated emotion model. Quoted claims, event severity and full-article aggregation distort interpretation.

- VADER source and threshold documentation: https://github.com/cjhutto/vaderSentiment/blob/master/README.rst
- NLTK implementation: https://www.nltk.org/api/nltk.sentiment.vader.html

**Supervised evaluation.** A stratified **80/20 train/untouched holdout split** with random state 42 estimates within-BBC predictive quality. For model selection, a stratified **five-fold cross-validation** on the training partition compares majority baseline, Multinomial Naive Bayes, Logistic Regression and linear SVM. The objective is macro-F1 because a strong aggregate accuracy could hide weak classes. Only after choosing and tuning the model on training folds do we evaluate the holdout once. Save accuracy, weighted/macro-F1, per-class precision/recall/F1, confusion matrix, error excerpts and feature ablation. The holdout is not reused to select features.

- Cross validation: https://scikit-learn.org/stable/modules/cross_validation.html
- Model selection: https://scikit-learn.org/stable/modules/grid_search.html

## 3. Hypotheses to test (not findings until actual run)

1. Category-specific news vocabulary should give TF-IDF linear models a substantial advantage over a majority-class baseline. Measure the training CV macro-F1 gap, and inspect terms actually selected.
2. Numerical and organizational references may vary across business and politics. Test through counts of `NUM`, `ORG` and `MONEY` per analyzed article. Avoid interpreting historical co-occurrence as a relationship.
3. Average VADER compound polarity may differ among beats, but quotations and vocabulary bias mean these differences are not automatically editorial mood. Compare means *and* per-category label proportions, not a cherry-picked single story.
4. Adding bigrams may help or hurt predictive performance given corpus size. Evaluate both n-gram ranges using training-only folds and report the actual difference.

## 4. Required measurement traceability

The trained notebook exports `run_manifest.json` (dataset hash and source, row counts, selected parameters, software versions and scores), `insights.json`, `model_cv_comparison.csv`, `per_class_metrics.csv`, `feature_ablation.csv`, `error_analysis_excerpt.csv`, `EVIDENCE_BASED_FINDINGS.txt` and eight figures. Use `python verify_release.py` to require all artifacts from a real-data run before calling the empirical phase complete. Do **not** copy the perfectly separable synthetic fixture's test scores into the report: those scores confirm code paths, not BBC classification quality.

## 5. Editorial business use and deployment boundaries

Newsroom editors can use routing suggestions to reduce initial triage effort if observed recall meets a documented desk-specific target. Media analysts can explore topic terms and mentions to prioritize human review. No external or temporal validation is included, so the system cannot be called production-ready. Before a pilot, validate on properly licensed recent multi-source news, test calibration/abstention thresholds, inspect false-positive NER and aliases, and record a versioned error audit without storing unnecessary personal information.

## 6. Course requirements and final evidence

The brief specifies all Modules 1–8, at least 500 substantive English articles in at least four categories, <=2,000 data points for Colab free tier, a public individual GitHub folder named `ITAI2373-NewsBot-Midterm`, a two-page reflection, and a PDF report with a **working GitHub link**. The assignment also includes a team-of-3–4 expectation and a separate dataset-approval rule. These administrative facts are not technical performance results and cannot be assumed resolved by an algorithm.
