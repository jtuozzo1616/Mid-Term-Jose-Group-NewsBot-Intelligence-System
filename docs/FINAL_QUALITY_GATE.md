# NewsBot — final evidence gate against the 100-point rubric

**Course:** ITAI 2373  
**Student:** José Miguel Tuozzo Izaguirre  
**Personal portfolio assignment folder:** https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm  
**Canonical code/results:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System  
**Successful full real-data workflow:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38775732890

| Rubric section | Max | Confirmed evidence | Remaining dependency |
|---|---:|---|---|
| Repository | 30 | Portfolio entry with the instructor's exact folder name and full-source notebook; public canonical code and reproducible evidence | Confirm Canvas URL format with teacher |
| Technical implementation | 30 | Eight NLP modules; 10 successful synthetic regression tests; complete real-data execution; five topic labels; Streamlit source | Actual free-tier Colab execution still for student to demonstrate if specifically requested |
| Analysis and insights | 30 | 1,440 labeled BBC articles; 1,152 train/288 holdout; tuned Linear SVM; 96.18% holdout accuracy, 0.9605 macro-F1; eight figures, class metrics, robustness and [results interpretation](Technical_Results_Summary.md) | Student must be able to explain observed findings; no claims for modern external news |
| Presentation and documentation | 10 | Seven-page PDF report, exactly two-page reflective PDF, portfolio README, recorded run evidence and video shot list | Reflection must be personalized; **video not recorded** |

## Verification boundaries

The latest passing GitHub Actions run includes ten software tests (synthetic fixtures), execution of the *historical BBC* labeled dataset notebook, real-output verification, aggregate result publication and executed notebook archive. The original 1,490 labeled records yielded **1,440 after exact-text deduplication**, five category labels, 1,152 train and 288 held out. Source SHA-256: `f56a65dab2ea728505a639d2186a2b2f1c0939f28e8e89b5ed1c1fe9520b1323`.

Holdout F1: business 0.9630; entertainment 0.9515; politics 0.9524; sport 0.9784; tech 0.9574. **11 of 288** held-out articles were classified incorrectly. This is within-source historical performance, not external validation or accuracy on today's news.

The root notebook intentionally has no stored output cells; generated PNGs/CSVs and a fully executed notebook are separately available through the passing workflow. Do **not** misrepresent an unexecuted GitHub notebook preview as a failed evaluation.

## Remaining human actions

1. **Get dataset permission:** the written instructor brief explicitly requires approval of the Kaggle dataset **before using it**. A request draft is included but a professor reply is not.
2. **Individual submission:** the published class brief expects 3–4 students. This repository discloses individual work; it does not falsely claim professor authorization or teammates.
3. **Personal reflection:** review the two-page PDF and ensure every contribution/lesson is true; disclose AI assistance as your course requires.
4. **Canvas:** actually submit the portfolio URL, required PDF(s) and any other requested links. GitHub itself cannot perform the Canvas hand-in.
5. **Optional video:** record a genuine 5–7-minute demonstration and add an accessible link to claim the video bonus; script alone does not qualify.

**Verdict:** technical and empirical components have strong documented support. Final 100/100 cannot be promised: the professor decides acceptance, rubric deductions and bonus eligibility.
