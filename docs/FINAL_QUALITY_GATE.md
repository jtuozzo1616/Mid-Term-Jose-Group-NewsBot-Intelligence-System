# NewsBot — Final grading quality gate and limitations

**Student:** José Miguel Tuozzo Izaguirre | **ITAI 2373** | **Scope:** Individual adaptation

## Instructor rubric mapped to verifiable evidence (100 base points)

| Component | Value | Evidence in this package | What cannot yet be declared complete |
|---|---:|---|---|
| Individual public GitHub repository | 30 | Organized `ITAI2373-NewsBot-Midterm` folder, README, Colab notebook, regression tests, dashboard, provenance and docs | Actual user-owned public repository must be created/published and link verified |
| Eight-module technical system | 30 | Module 1 purpose+data, 2 cleaning/tokens/lemmas, 3 TF-IDF, 4 POS, 5 dependencies/SVO, 6 VADER/emotion proxies, 7 four classifiers + heldout metrics, 8 NER/co-mentions; interactive demo + release verifier | The complete workflow has not yet been executed on actual BBC data in this isolated environment |
| Analysis and business insights | 30 | Seven core charts + one advanced stress chart, per-class precision/recall/F1, confusion matrix, CV, tuning, term interpretation, error excerpts, bootstrap interval, run hash, business interpretation | Actual figures, scores and observed results generated only during a real BBC run; no placeholder can replace them |
| Presentation and documentation | 10 | Professionally formatted technical PDF, exactly two-page individual reflection, script for optional six-minute video, research citations | Report remains marked pre-run and lacks actual repository URL; optional video cannot be recorded/uploaded by code |

## Execution verification

- `python -m unittest discover -s tests -p 'test_*.py' -v`: **8 synthetic regression tests passed** in the present isolated environment; no claim about real BBC model quality.
- `python -m py_compile dashboard.py generate_final_report.py generate_individual_reflection.py verify_release.py run_all_and_package.py`: source syntax passes.
- Notebook: **36 cells** with eight modules and an additional explicitly labeled robustness extension.
- `docs/NewsBot_Reflection_Solo.pdf`: two pages, no fabricated collaborators.
- `docs/MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf`: three-page research-methods draft; it will be regenerated with real plots and numeric findings once the notebook has executed.
- Source BBC competition official description: 1,490 labeled training articles and five classes. The optional research mirror is documented separately, and the original BBC copyright remains intact.

## Why a 100/100 cannot yet be guaranteed

A code audit is not a blind 100-point grade. Three external conditions matter: **real-data execution**, **working GitHub repository**, and any instructor-specific interpretation of the original team/dataset requirements. Course grading and approval decisions cannot be supplied by this package. The full BBC corpus and pretrained spaCy model were not available as mounted attachments or installable resources in the isolated build environment, and outbound network retrieval from that runtime failed. Do not publish synthetic accuracy of 1.000 as empirical news accuracy.

## Fast route to a demonstrably complete submission

1. Upload the provided ZIP to Google Colab; unzip it, `cd ITAI2373-NewsBot-Midterm`, and execute the commands in README section **Streamlined end-to-end execution**. The notebook tries a documented public research mirror if `BBC News Train.csv` was not uploaded, and records the exact SHA-256 of the input.
2. Download the generated `NewsBot_VERIFIED_EXECUTION_EVIDENCE.zip` after the script prints a real-data PASS. Inspect class metrics, the most frequent confusions, VADER and POS charts.
3. Regenerate and personally verify the individual reflection. Verify that PDF still has exactly 2 pages; author must confirm first-person learning claims are accurate.
4. Publish the permitted project assets under your own GitHub repository, verify the public URL, and regenerate the report with `--repo` containing that precise link. Do not upload licensed article texts or credentials.
5. Optional: record the 5–7-minute demonstration following `docs/Video_Demo_6_Minute_Script.md`, including new articles and observed numbers, then add the verified video URL.

## Transparency rules

The synthetic 525-row fixture is constructed from obvious category vocabularies only to test code paths; 100% fixture accuracy is neither surprising nor reportable as BBC evaluation. The spelling stress test is an **artificial perturbation** of in-domain holdout articles, not publisher or temporal generalization. The bootstrap confidence interval estimates sampling variability conditional on that old corpus and split; it does not address editorial domain shift. The basic emotion word list is not a validated emotion classifier. Co-mentions are not verified relationships.
