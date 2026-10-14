# Quality assurance — verified project state (October 2026)

A successful [full evaluation workflow](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38491913062) installed dependencies, passed **10 regression tests on synthetic fixtures**, executed all eight NLP modules against historical BBC articles, ran `verify_release.py`, published non-article aggregate results, and retained the executed notebook/evidence archive.

**Actual recorded BBC evaluation:** 1,440 articles retained after exact deduplication; 1,152 training, 288 independent holdout; tuned linear SVM; macro-F1 = 0.9605 and accuracy = 0.9618. The source SHA-256 and software versions are in `outputs/run_manifest.json`. Published outputs include eight figures, model comparison, per-class precision/recall/F1, an ablation, an error-count summary, stress-test results and bootstrap uncertainty.

**Important distinctions:**
- The synthetic unit tests verify software paths; they are not dataset performance.
- The root Jupyter notebook in Git is a clean *runnable* notebook with no saved cell outputs; the *executed* notebook is in the successful Actions run's downloadable evidence archive. Figures and aggregated scores are published separately.
- A seven-page technical PDF and an exactly two-page reflection PDF are present. The reflection remains subject to the student's factual, firsthand review.
- Results measure in-distribution BBC performance only. No external multi-publisher or 2026 generalization has been tested.
- The optional video is a script, not a recorded video. Instructor permissions and Canvas submission are not proven by CI.

See `docs/FINAL_QUALITY_GATE.md` and `docs/Execution_and_Submission_Checklist.md` for what is verified versus what remains for the student.
