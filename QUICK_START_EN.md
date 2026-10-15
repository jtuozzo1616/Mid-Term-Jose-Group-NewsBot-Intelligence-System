# NewsBot — quick start

**ITAI 2373 · José Miguel Tuozzo Izaguirre**  
[Main repository](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System) · [Course portfolio](https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm) · [Professor's review guide](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/PROFESSOR_REVIEW_GUIDE.md)

## Inspect the finished work

- **Notebook:** [Midterm_NewsBot_Intelligence_System.ipynb](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/Midterm_NewsBot_Intelligence_System.ipynb) — complete code for all eight NLP modules.
- **Completed notebook (permanent):** [NewsBot_Executed_Results.ipynb](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/NewsBot_Executed_Results.ipynb) — open directly to review saved outputs.
- **Execution verification:** [successful GitHub Actions run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38778575638).
- **Measured results:** [outputs/](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/tree/main/outputs) — eight figures, class-level metrics, confusion matrix, model and run manifest.
- **Error analysis:** [11 measured holdout misclassifications](docs/HOLDOUT_ERROR_CASE_STUDY.md), with [count-only confusion directions](outputs/error_directions.csv).
- **Reports:** [technical PDF](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/MT_Report_Group_Solo_Jose_Miguel_Tuozzo_Izaguirre_ITAI2373.pdf) and [two-page reflection](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/NewsBot_Reflection_Solo.pdf).

The root notebook is intentionally clean and runnable; the completed notebook is separately committed to both the main repository and the course portfolio, so reviewers do not have to download expiring workflow artifacts.

## Run the project in Google Colab

1. [Open the one-click Colab launcher](https://colab.research.google.com/github/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/RUN_NEWSBOT_IN_COLAB.ipynb).
2. Select **Runtime → Run all** and allow time for spaCy and the classifier comparisons.
3. Read the verification result and download the generated ZIP of execution evidence.

The runner obtains a documented research copy of the **labeled historical BBC News Train.csv** when none is supplied. To comply with course approval or data-access rules, provide the official Kaggle training CSV if requested by your instructor. Do not use the competition's unlabeled test file for an accuracy evaluation.

For local execution:

```bash
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python run_all_and_package.py --github "https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System"
python verify_release.py
python verify_error_audit.py
```

## What to expect

The completed GitHub run retained **1,440** labeled historical BBC articles, used **1,152** for training and **288** for testing, and selected **Linear SVM**. Test accuracy was **96.18%** (277 correct), with **0.9605 macro-F1**. The results describe the BBC corpus, not modern multi-publisher news. This is a research and editorial-assistance prototype, not a fact checker.

See the [evaluation explanation](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/Technical_Results_Summary.md), [video demonstration guide](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/Video_Demo_6_Minute_Script.md) and [submission checklist](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/blob/main/docs/Execution_and_Submission_Checklist.md).

**Before submitting:** Check that the reflection describes your actual experience and that the instructor's dataset and assignment-format requirements have been met. Add the video link when you have uploaded the recording.
