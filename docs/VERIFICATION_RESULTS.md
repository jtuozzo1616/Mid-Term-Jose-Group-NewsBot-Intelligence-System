# Verified execution log

- Repository: https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System
- Live run: https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38488603289 — **success**.
- Artifact publication: https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38489270753 — **success**.
- 10 software regression tests (synthetic fixtures): **passed**, distinct from BBC model metrics.
- BBC dataset provenance: outputs/run_manifest.json, label counts in outputs/insights.json; SHA-256 fingerprint recorded.
- Retained labeled BBC articles: 1440; train 1152; unseen holdout 288.
- Selected model: tuned Linear SVM with class balancing and TF-IDF (ngram range 1–2, max_features 10000, C=2).
- Training-only 5-fold CV macro-F1 0.9801; independent holdout macro-F1 0.9605 and accuracy 0.9618.
- Five class-level F1 scores from outputs/per_class_metrics.csv; eight figures and source-safe aggregate tables published in outputs/.
- Generated technical report: 8 pages; generated individual journal: **exactly 2 pages**, measured with PDF page metadata and visual render.
- Model file: outputs/newsbot_classifier.joblib; only load after verifying the trusted repository provenance.
- The full executed notebook and full permitted course evidence archive are accessible from the successful Actions run.

## Cautions
The dataset is historical and from a single publisher. The emotion feature is an illustrative word lexicon; syntax triples and entity co-mentions are heuristics. Classifier scores outside the historical distribution are not calibrated real-world probabilities. Group/solo and dataset approval requirements remain administrative decisions for the instructor. The student must review and personalize the reflective journal before submission.
