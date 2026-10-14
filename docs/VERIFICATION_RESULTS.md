# Verified local technical checks — 2026-10-13

- Python files `dashboard.py`, `generate_final_report.py`, `reflection.py`, `verify_release.py`, `run_all_and_package.py`: syntax compiled.
- Notebook `Midterm_NewsBot_Intelligence_System.ipynb`: validated with nbformat 4.5, 36 cells.
- `python -m unittest discover -s tests -p "test_*.py" -q`: **8 tests passed**. Tests cover notebook parseability, Kaggle schema variants, duplicate removal, rejection of unlabeled test input, fallback provenance with a mocked download, real-output guard failure on missing files, the classification pipeline, and the robustness/uncertainty extension. All fixture articles are SYNTHETIC.
- PDF check: `NewsBot_Reflection_Solo.pdf` **exactly 2 pages**.
- PDF check: `MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf` **3 pages** in its current pre-run state; contains no manufactured macro-F1.
- No labeled BBC dataset mounted locally, no installed trained spaCy language pipeline and no actual BBC output metrics available in this environment. The user-facing release automation requires a REAL_DATA_EXECUTED manifest and all saved files.

**Do not interpret the synthetic fixture's high/100% accuracy as a real BBC result.**


**Current workflow:** [Verified BBC Evaluation](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/workflows/newsbot-verify.yml). Synthetic local tests are separate from historical BBC held-out model scores. Refer to outputs/run_manifest.json and the latest green workflow for actual figures; do not substitute test-fixture scores.
