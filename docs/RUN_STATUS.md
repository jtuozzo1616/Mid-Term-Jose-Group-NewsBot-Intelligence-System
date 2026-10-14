# Verified-run status and interpretation

Repository: https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System

The source code is public, and regression tests run on **synthetic fixtures**. Smoke tests do not measure classification quality on BBC articles.

A successful [Verified BBC Evaluation workflow](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/workflows/newsbot-verify.yml) creates: all eight NLP modules; labeled BBC source provenance and hash; training-only five-fold model selection; independent held-out macro-F1 and accuracy; five category scores; eight charts; sensitivity and bootstrap analysis; two PDF documents; and the executed notebook in an evidence archive.

**Evidence rule:** outputs/run_manifest.json must be generated during the real-data notebook run, verify_release.py must pass, and the GitHub Actions workflow must show green. Do not cite synthetic test metrics.

**Copyright:** BBC articles, error excerpt files, credential files and full dataset CSV must not be published as public repository source. Any downloaded evidence archive is for course review subject to its source rights.

**Professor-controlled conditions:** The rubric originally requires groups of 3–4, an approved Kaggle dataset, and an ITAI2373-NewsBot-Midterm folder in an individual portfolio. This separately hosted solo repository follows the student's stated preference, but instructor acceptance is unverified. The reflection must be reviewed and personalized by the student; optional demo recording is not included.
