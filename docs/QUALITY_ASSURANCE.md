# Quality assurance

The submitted notebook's cells are valid, all eight Python unit/regression tests pass locally, and the two required-style PDFs build without layout errors. Article loader rejects a missing category and exact-text duplicates are removed before cross-validation. Test fixtures are completely synthetic and cannot establish real-news model accuracy. `verify_release.py` refuses to attest missing real-data artifacts, and report generation falls back to a prominently labeled pre-run version rather than inventing empirical evidence.

Upon genuine execution on 1,490 labeled BBC training rows (minus justified cleaning), inspect the saved confusion matrix, class metrics, sentiment/NER patterns, stress test, and SHA-256. Verify the final public GitHub URL and regenerate the report. The optional six-minute demonstration remains a storyboard until recorded by the student.
