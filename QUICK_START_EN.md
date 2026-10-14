**Published standalone project:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System

# NewsBot Midterm — Exact Completion Procedure (English)

**Course:** ITAI 2373 | **Student:** José Miguel Tuozzo Izaguirre | **Goal:** evidence-based submission against every 100-point requirement.

## What is already implemented

The complete English Jupyter notebook contains all eight modules, syntactic and lexical feature analysis, VADER sentiment, an illustrative emotion dictionary, PERSON/ORG/GPE/DATE/MONEY extraction, duplicate checks, four-model comparison (including baseline), training-only five-fold CV, train-only parameter tuning, untouched holdout testing, confusion and entity plots, and an integrated prediction class. A Streamlit dashboard is included as an optional bonus opportunity.

**Critical distinction:** An executable notebook is not the same as executed evidence. The official BBC News Train.csv is not embedded in this ZIP. Dataset authorization is not presumed. No actual BBC macro-F1 is claimed in this package.

## Finalize in order

1. **Instructor approval (mandatory):** Open `docs/Dataset_Approval_Request.md`, verify the dataset examples, request permission for both the dataset and a solo submission, and email it to the instructor. Wait for written authorization. The sample record IDs and titles were cross-checked against a publicly visible mirror, but the dataset must be obtained under Kaggle competition rules.
2. **Access the data (mandatory):** Visit https://www.kaggle.com/competitions/learn-ai-bbc/data, sign in, accept the competition rules, and download `BBC News Train.csv` (1,490 labeled rows). **Do not use** `BBC News Test.csv`, which has no category labels. Never upload raw copyrighted article text to a public repository.
3. **Colab setup:** Upload `Midterm_NewsBot_Intelligence_System.ipynb` to https://colab.research.google.com and use the Files panel to upload `BBC News Train.csv` into `/content`. The notebook accepts `ArticleId,Text,Category` and also recognizes mirrors with the text header `Article`. **Run all**. If installation requests restart, restart and run all again. No GPU or paid resources are required.
4. **Validate real analysis:** Confirm final dataset >= 500 records and 5 labels; eight saved figures; all output files; meaningful POS, NER and VADER summaries; a realistic confusion matrix and per-category metrics; all 3 new fictional article predictions; no exceptions. Look for `PASS: notebook produced...` at the end.
5. **Copy evidence:** From the Colab Files panel, download the `outputs/` folder's figures, metrics, `run_manifest.json` and `insights.json` to the local `outputs/` directory. Keep the large `newsbot_classifier.joblib` for your dashboard; it is intentionally ignored by Git.
6. **Generate a genuine final report:** Install project requirements and ReportLab in your local environment, then run:

   ```bash
   python -m pip install -r requirements.txt reportlab pillow
   python generate_final_report.py --group "Solo" --repo "https://github.com/USERNAME/ACTUAL_REPOSITORY"
   ```

   The report generator imports **your actual execution results** from `outputs/`. If missing, it clearly creates an unverified draft rather than making up accuracy. Read the complete PDF and add your evidence-based methodological observations if needed.
7. **Complete reflection:** Complete the English two-page *individual* reflection using authentic decisions, technical setbacks, real results once available, and your sole contributions. Export to exactly two pages as `NewsBot_Reflection_Solo.pdf`. Do not invent teammates or meetings; get written solo-submission approval.
8. **Publish separately:** Publish the completed notebook and permissible results to your **public individual GitHub portfolio**, under `Mid-Term-Jose-Group-NewsBot-Intelligence-System/`. Check the URL signed out. Confirm with the instructor how Canvas should receive the mandatory reflection from an approved solo student.
9. **Optional video:** Film 5–7 minutes with two never-before-seen articles, show results and at least two plots, explain an actual finding and business value; upload unlisted and link it in the README. The instructor notes optional video bonus points but also assigns presentation/documentation points; confirm how that affects base grading.

## Known boundaries and integrity

- Historical BBC topics: business, entertainment, politics, sport and tech. There is **no Health category** in this selected dataset.
- VADER is a lexical tone tool, not a truth detector or perfect description of author intent.
- Entity co-mentions do not show real-world affiliation. POS and parse analysis is truncated at 3,500 characters per article; supervised classifier uses full text.
- For linear SVMs, model decision margins are not calibrated probabilities; the demo's manual-review warning is an explicitly illustrative heuristic.
- The instructor requires the student's original research, interpretation, design explanations and personal reflection. Revise these based on authentic work and what the executed cells prove.

## Main files

- `Midterm_NewsBot_Intelligence_System.ipynb` — expanded instructor-template notebook.
- `generate_final_report.py` — automatic, actual-results-aware technical PDF.
- `dashboard.py` — optional Streamlit demo (requires locally generated model).
- `tests/` — checks for data loading, normalization and model training.
- `docs/NewsBot_Reflection_Solo.pdf` — exactly two-page *individual working draft*.
- `docs/Dataset_Approval_Request.md` — ready to customize and email.
- `docs/Submission_Audit_100_Point_Rubric.md` — rubric-by-rubric check.

## 2026-10-13 enhancement: Automatic end-to-end release check

The notebook can fetch a **public research mirror** of the labeled competition CSV if none has been uploaded; the fetched source and SHA-256 are preserved in the manifest (see README for data rights). For the complete project folder in Colab, run `python -m pip install -r requirements.txt nbclient nbformat reportlab pillow`, install `en_core_web_sm`, and execute `python run_all_and_package.py --github "https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System"`. This creates a verified execution ZIP with the executed notebook, eight figures, metrics, report and reflection. This build's offline regression checks cannot replace the real-data run.


## Tested automation on GitHub Actions

Use the [Verified BBC Evaluation workflow](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/workflows/newsbot-verify.yml) in Actions → Run workflow. It checks local code tests first, registers a Python 3 Jupyter kernel, executes the notebook against the **real BBC training CSV**, regenerates the academic PDF and two-page reflection draft, and creates the verified evidence archive. A green workflow and outputs/run_manifest.json are required before citing holdout scores.

The standalone repository is already created; do not create another. The original course rubric's portfolio-folder and solo/group restrictions are independent instructor decisions that the software cannot waive. The named student's final reflection must be personally reviewed.
