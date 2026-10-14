# NewsBot Midterm — current execution and submission instructions

**Student:** José Miguel Tuozzo Izaguirre | **Course:** ITAI 2373  
**Canonical project:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System  
**Personal portfolio folder:** https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm

## What has actually completed

The eight-module notebook has been executed on a historical labeled BBC dataset by [a successful GitHub Actions workflow](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38491913062). The results in the repository are **1,440 retained articles**, **288 held-out test articles**, **96.18% accuracy** and **0.9605 macro-F1**; they are not synthetic unit-test metrics. All eight figures, a model artifact and generated reports are in the canonical project. See [run status](docs/RUN_STATUS.md).

## Recommended submission path

1. Use the course-named `ITAI2373-NewsBot-Midterm` folder in the [personal portfolio](https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm) as your individual portfolio entry. The linked canonical project contains the working source, reproducibility commands and result artifacts.
2. Submit the [technical PDF](docs/MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf) and the required [exactly two-page reflection](docs/NewsBot_Reflection_Solo.pdf) as the instructor's Canvas instructions permit. **Read and personalize the journal first**: technical metrics can be automated, personal learning and teamwork cannot.
3. Check that the professor has actually approved the BBC Kaggle dataset, as the assignment explicitly requires pre-approval. The [request draft](docs/Dataset_Approval_Request.md) is not approval.
4. The work is identified as individual/solo. The original instructions say groups of 3–4; only the instructor can approve another arrangement. Do not claim collaboration that did not happen.
5. The optional recorded 5–7 minute video can earn bonus credit if completed and linked. [Script and shot list](docs/Video_Demo_6_Minute_Script.md) are available, but the recording is not included.
6. Open the repository and PDF links in a logged-out browser and upload the correct URLs and files to Canvas. **A code repository alone does not submit a Canvas assignment.**

## Re-execute in Colab, with all evidence

[Open the one-click Colab notebook](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/RUN_NEWSBOT_IN_COLAB.ipynb), select **Run all** and check the runtime report. It clones the canonical project, fetches the documented BBC competition-file mirror when needed, runs the full notebook and downloads `NewsBot_VERIFIED_EXECUTION_EVIDENCE.zip`. To comply with dataset-use terms and pre-approval, prefer uploading the official labeled Kaggle `BBC News Train.csv` if required by your instructor. The unlabeled Kaggle test CSV cannot be used for the supervised evaluation.

For local reproduction:
```bash
python -m pip install -r requirements.txt nbclient nbformat reportlab pillow
python -m spacy download en_core_web_sm
python run_all_and_package.py --github "https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System"
python verify_release.py
```

The experiment compares four model families, uses five-fold cross-validation *only within training*, avoids TF-IDF leakage, and evaluates a separate holdout. Its linguistic, sentiment and NER analyses are exploratory, limited by BBC's historical single-source distribution. See [empirical results](docs/Technical_Results_Summary.md) and [quality gate](docs/FINAL_QUALITY_GATE.md).

**Last reviewed:** October 2026. No claims are made of instructor permission, a live deployment or a student-recorded video.
