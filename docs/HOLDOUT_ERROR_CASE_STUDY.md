# Where NewsBot gets confused: a holdout error audit

**ITAI 2373 · NewsBot Intelligence System · José Miguel Tuozzo Izaguirre**

**Evidence:** [executed notebook](NewsBot_Executed_Results.ipynb) · [confusion matrix](../outputs/06_confusion_matrix.png) · [nine observed error directions](../outputs/error_directions.csv) · [per-class evaluation](../outputs/per_class_metrics.csv) · [run manifest](../outputs/run_manifest.json)

## The result, and what it does not say

The best training-side model was **Linear SVM** with TF-IDF unigrams and bigrams. After model selection, it received **288 BBC articles withheld from training** and classified **277 correctly**. Holdout accuracy was **96.18%** and macro-F1 was **0.9605**. This is a strong result within the historical BBC corpus, **not** a measured claim about news published today.

A single overall accuracy figure hides two different risks:

- **Missed stories:** an article belonging to a desk is sent somewhere else (false negative for the correct desk).
- **Misrouted stories:** an editor receives an article that actually belongs to another desk (false positive for the predicted desk).

Both matter when evaluating whether NewsBot could support human-reviewed news routing.

## What the 11 errors actually were

The table below comes from the **11 incorrectly predicted holdout articles** in the verified GitHub Actions execution. The counts, not article text, are published here so that the audit remains inspectable without redistributing BBC reporting.

| Actual BBC category → NewsBot prediction | Errors | Plausible overlap noticed during review |
|---|---:|---|
| tech → business | **2** | Video-game developers facing sales, ownership or financial pressure |
| entertainment → tech | **2** | Music-consumption statistics and a television format enabled by technology |
| business → sport | 1 | Financial-market discussion about a football club |
| politics → entertainment | 1 | Personal-life coverage of a public official |
| entertainment → politics | 1 | Broadcasting oversight and government scrutiny |
| politics → business | 1 | Public spending controls and financial irregularities |
| entertainment → sport | 1 | A sporting achievement presented as a television moment |
| politics → sport | 1 | A political figure's sports-related anecdote |
| business → politics | 1 | Pensions research with public-policy implications |
| **Total** | **11** | |

These thematic notes **describe the sampled errors**, rather than proving why the model made each decision. A linear TF-IDF model responds to lexical patterns; to establish the precise reason for one prediction, we would need to examine its weighted features and compare them with a suitable counterfactual article. The original article excerpts remain inside the restricted execution archive and have **not** been copied into this public repository.

Two confusion directions occurred twice; the other seven appeared once each. It would be an overstatement to describe one-off errors as a stable systematic bias.

## Interpreting precision and recall without exaggeration

| BBC class | Held-out articles | Correctly recognized | Sent elsewhere | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| business | 67 | 65 | 2 | 97.01% | 0.9630 |
| entertainment | 53 | 49 | **4** | **92.45%** | **0.9515** |
| politics | 53 | 50 | 3 | 94.34% | 0.9524 |
| sport | 68 | 68 | **0** | **100%** | 0.9784 |
| tech | 47 | 45 | 2 | 95.74% | 0.9574 |

**Entertainment is the weakest class by F1.** Four of its 53 labeled articles were sent to another desk. A useful editorial control would be to review entertainment stories involving government oversight, sports celebrities or digital platforms before relying on their proposed label.

**Sport shows why precision and recall must be reported together.** The model identified all 68 actual sport articles, so its recall was **100%**. Nevertheless, it mistakenly labeled **three non-sport articles** as sport; sport precision was only **95.77%**. Perfect recall on 68 held-out articles does not mean sport predictions are always correct.

**Business illustrates incoming misroutes.** Two actual business articles were missed, while three articles belonging to other categories were sent to business. Thus, a newsroom desk might see apparently high recall and still spend time rejecting unrelated material.

## What I would change, and how I would test the changes

1. **Introduce a human-review route for ambiguous cross-topic stories.** An editor should inspect articles involving business deals in sports, the economics of technology, or policy questions appearing in entertainment coverage. The review rule needs a clearly specified workload and cannot be judged from this holdout alone.
2. **Measure precision and recall by editorial desk, not accuracy alone.** Entertainment recall (92.45%) and sport precision (95.77%) point to different operational problems. Track false deliveries and missed relevant items separately.
3. **Calibrate scores before introducing a numerical confidence threshold.** The SVM's raw margins and their softmax transforms are **not calibrated probabilities**. Any abstention threshold should be selected using training-side validation, then assessed once on a new test set.
4. **Test on newer, multi-publisher articles.** Historical UK BBC vocabulary may not reflect today's source mix. A fresh evaluation should check whether the same confusion directions recur or disappear.
5. **Review actual feature contributions.** Study the most influential TF-IDF tokens for each mistake, and test whether different training examples or domain-specific features reduce errors. The holdout must **not** be reused to tune features or report a newly optimized score.

## Reproducibility and evidence boundaries

- The [machine-readable error directions](../outputs/error_directions.csv) contain only actual and predicted **category labels** and aggregate counts. Their total is 11.
- The [class-level metrics](../outputs/per_class_metrics.csv) and [confusion matrix](../outputs/06_confusion_matrix.png) describe the same 288 holdout predictions.
- The [manifest](../outputs/run_manifest.json) records the 1,440 retained articles, 80/20 split, random seed, selected parameters and source SHA-256. The [fully executed notebook](NewsBot_Executed_Results.ipynb) records the underlying experiment.
- The small spelling-perturbation experiment is a **single bounded sensitivity check**. Its slightly higher score on one noisy run is not proof of improved model robustness.
- The classifier **does not check facts**, and the source has no Health category. The confusion study does not establish real-world editorial effectiveness or performance on other publishers.

**Main conclusion:** The useful insight is not that NewsBot has a 96% score. It is that most articles are organized correctly in this corpus, while several believable intersections between editorial topics produce errors that an actual newsroom would need a transparent review process to handle.
