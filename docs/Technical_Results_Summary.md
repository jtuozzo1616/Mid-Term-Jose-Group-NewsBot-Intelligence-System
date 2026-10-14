# NewsBot Intelligence System — empirical technical findings

**Course:** ITAI 2373, Modules 1–8  
**Student:** José Miguel Tuozzo Izaguirre  
**Evidence:** [real-data successful workflow](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38491913062), [run manifest](../outputs/run_manifest.json), [full analytical notebook](../Midterm_NewsBot_Intelligence_System.ipynb), [technical PDF](MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf).  
**Scope:** historical BBC articles (2004–2005), **not** live/news-of-2026 reporting.

## 1. Evaluation design and dataset provenance

The source was a public research mirror of Kaggle's *BBC News Classification* labeled 1,490-article training file, not the competition's unlabeled test file. Before splitting, the pipeline removed **50 exact-text duplicates** and zero missing articles, leaving **1,440** English articles from five classes: sport 342, business 335, politics 266, entertainment 263 and tech 234. The model training partition had **1,152** articles; **288** were reserved for final evaluation. The script records the dataset source and SHA-256 so others can distinguish this corpus from unrelated fixtures.

Training-side five-fold stratified cross-validation is used to select model families and TF-IDF/regularization hyperparameters, with feature fitting confined to the pipeline's training folds. This reduces vocabulary leakage. The untouched holdout measures performance within the historical BBC distribution; the data source is not independent external 2026 news. The public repository omits copyrighted source article text.

## 2. Four classifiers and holdout assessment

| Model family | Five-fold training macro-F1, pre-tuning |
|---|---:|
| Linear SVM | 0.9782 |
| Logistic Regression | 0.9692 |
| Multinomial Naive Bayes | 0.9681 |
| Dummy majority | 0.0769 |

After training-only tuning, Linear SVM with `C=2`, TF-IDF unigrams+bigrams and 10,000 maximum features attained mean CV macro-F1 **0.9801**. It then achieved **0.9618 holdout accuracy** (277/288 correct), **0.9605 macro-F1**, and **0.9616 weighted-F1**. The 800-resample bootstrap interval for holdout macro-F1 was **0.9334 to 0.9800**; it measures resampling uncertainty under this dataset and does not capture external dataset shift.

| Holdout category | Precision | Recall | F1 | Articles |
|---|---:|---:|---:|---:|
| business | 0.9559 | 0.9701 | 0.9630 | 67 |
| entertainment | 0.9800 | 0.9245 | 0.9515 | 53 |
| politics | 0.9615 | 0.9434 | 0.9524 | 53 |
| sport | 0.9577 | 1.0000 | 0.9784 | 68 |
| tech | 0.9574 | 0.9574 | 0.9574 | 47 |

**Editorial takeaway:** entertainment is the weakest class by F1, and its recall is 0.9245, so several entertainment articles would require human review instead of invisible routing. Sport had all 68 holdout items recovered (recall 1.0000), **not** evidence that sport predictions are always correct or that a model will generalize across publishers. The actual confusion summary includes two tech→business and two entertainment→tech errors; a cross-category article containing commercial or digital media terms may be genuinely ambiguous.

## 3. TF-IDF, POS and syntax observations

The most category-distinctive TF-IDF terms include **growth / shares / market** for business; **film / actor / awards** for entertainment; **labour / election / blair** for politics; **game / win / cup** for sport; and **users / software / technology** for tech. These discriminative terms explain why TF-IDF-based topic classifiers separate historical BBC beats well, while the named politics terms also signal that the corpus is rooted in a particular 2004–2005 UK period.

**Ablation:** training CV macro-F1 increased from **0.9776** for unigrams to **0.9801** for unigrams+bigrams, an absolute **0.0025** improvement. This is a modest within-sample gain; it should not be described as a broad generalization result.

Relative POS ratios differ: tech has a **0.2620** mean NOUN share versus **0.2082** in sport; sport has **0.1048** PROPN share versus **0.0500** in tech. Sport uses a relatively high proportion of named entities and pronouns; tech features more common nouns. The dependency parser estimates **10.782** passive markers per sampled politics article versus **4.927** in sport, but these are descriptive counts from text truncated to the first 3,500 characters per article. The dependency-based SVO triples approximate grammatical relations, **not** verified semantic roles.

## 4. Sentiment, entities and relations

Mean VADER compound sentiment by topic: **entertainment 0.5900**, **sport 0.5492**, **tech 0.5330**, **business 0.2381**, **politics 0.0541**. This lexicon-based difference is descriptive, not evidence that journalists endorse positive/negative events or that politics is unbiased. Quotations, article length and category vocabulary confound whole-article sentiment. The emotion dictionary is a teaching proxy, not a validated classifier.

Extracted target entity-type mentions: **DATE 8,274**, **PERSON 7,482**, **GPE 5,222**, **ORG 4,149**, **MONEY 1,667**. Raw mention counts are not unique people/places; NER can mistake aliases or lowercased names. The top co-mention pair `blair` / `tony blair` appeared 50 times and likely refers to the **same person under two surface forms**—a clear reason to normalize entity aliases before inferring networks. Co-mention edges are never evidence that two entities share a real causal, organizational or personal relationship.

## 5. Robustness and business decision

With a frozen trained model, a deterministic stress test changed a small subset of long words in holdout articles. Macro-F1 moved from **0.9605** to **0.9639**; a slight increase does **not** demonstrate better robustness, because it is one noisy perturbation against the same holdout and the effect is small. Repeat with multiple perturbation strengths/seeds and external news before drawing deployment conclusions.

A reasonable newsroom prototype would **suggest** desk assignment and flag cross-category/uncertain cases for human review. To measure actual business value, collect time-to-triage, human override rates, category-specific recall, false-positive entities, and performance by publisher and date. Do not automate publication or rely on SVM margin softmax outputs as calibrated confidence scores.

## 6. Reproducibility, limits and next steps

- [Eight figures](../outputs/) cover corpus distribution, class terms, language patterns, entities, model CV, confusion, co-mentions and robustness.
- [Run manifest](../outputs/run_manifest.json), [classification report](../outputs/classification_report.txt) and [full summary JSON](../outputs/insights.json) let an evaluator reproduce the numeric claims.
- [Unmodified main notebook](../Midterm_NewsBot_Intelligence_System.ipynb) can be re-run on Colab; the fully **executed** notebook is provided as a successful GitHub Actions artifact.
- No external multi-source evaluation, probability calibration or production deployment is claimed. The BBC dataset **does not contain Health**. Source article text is not published in the repo.
- The instructor's pre-approval and individual/group grading instructions remain external administrative questions, not technical results.

**References:** [BBC Kaggle dataset](https://www.kaggle.com/competitions/learn-ai-bbc/data); [original corpus attribution](https://github.com/derekgreene/bbc-datasets); [scikit-learn](https://scikit-learn.org/stable/); [spaCy](https://spacy.io/); [NLTK VADER](https://www.nltk.org/api/nltk.sentiment.vader.html).
