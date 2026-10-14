# NewsBot — evidence-based alignment 
**Student:** José Miguel Tuozzo Izaguirre | **Course:** ITAI 2373  
**Portfolio:** https://github.com/jtuozzo1616/Jose-Tuozzo-AI-Portfolio/tree/main/ITAI2373-NewsBot-Midterm  
**Canonical source:** https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System

| Instructor rubric | Maximum | Evidence currently available |
|---|---:|---|
| GitHub repository | 30 | Named public portfolio folder; canonical notebook, README, code, automated tests, charts, aggregate CSV/JSON, experiment manifest |
| Technical implementation | 30 | All eight NLP modules completed in a [successful real-data run](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System/actions/runs/38491913062); end-to-end demo on fictional articles; optional dashboard source |
| Analysis and insights | 30 | 1,440 BBC articles, tuned SVM, holdout accuracy **0.9618**, macro-F1 **0.9605**, class-level and confusion analysis, ablation, actual category-level linguistic statistics |
| Presentation and documentation | 10 | Seven-page technical PDF, two-page reflective journal draft, README, Colab launcher and demo script; **no recorded demo evidenced** |

### Results, not promises

- Main experiment: 1,152 training + 288 untouched test articles from five BBC categories.
- 11 holdout errors out of 288. Lowest holdout F1: entertainment (0.9515); highest: sport (0.9784).
- Cross-validated macro-F1: tuned SVM **0.9801**, versus dummy majority baseline **0.0769** (untuned comparison). Compare like with like.
- All ten synthetic software tests passed; these do **not** replace the heldout model evaluation.
- Figures and scores are in the public repository; the executed notebook is attached to the passing GitHub Actions run. All findings are from historical BBC and are not externally validated.

### Outstanding grading dependencies

1. **Dataset approval:** the rubric demands instructor pre-approval for any Kaggle dataset; no approval reply is stored.
2. **Individual-vs-group arrangement:** the assignment states teams of 3–4; do not assert it was waived.
3. **Reflection:** personally verify and revise the exact two-page text before submission.
4. **Canvas submission:** no evidence of uploaded URLs/PDFs or rubric acceptance is available.
5. **Optional video:** no student-recorded demonstration link is published; script alone is not the bonus.
6. **Colab-specific instruction:** full pipeline executed in GitHub Actions; the user should additionally run it in Google Colab if that exact platform is mandatory for grading.

**Conclusion:** The technical work supports a strong score, but 100/100 is not provable or guaranteed by a self-audit. Only the instructor grades the submission.
