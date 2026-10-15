# What NewsBot Taught Me

**Personal Reflective Journal | ITAI 2373**  
**Student:** José Miguel Tuozzo Izaguirre

*Review draft: the first-person observations and stated learning must be checked and revised by the student before academic submission. The numerical results are grounded in the completed BBC evaluation.*

## 1. Collaboration, planning, and ownership

The most important shift in my thinking was learning to see NewsBot as one system instead of eight unrelated assignments. Each module has a purpose, but the value appears when the results support one another. A clean article becomes a reliable input for linguistic analysis; TF-IDF turns text into features; the classifier suggests a category; and sentiment and entities give a reader more context. Planning these connections taught me to ask what a result would mean to an editor before deciding what to calculate. I also learned that organizing work into small, inspectable stages makes problems easier to locate than trying to debug a large notebook all at once.

Because I am presenting the project under my own name, I need to be able to explain the design and defend the findings rather than rely on a checklist of completed cells. I have learned to use documentation, clear variable names, repeated tests, and the published execution record as ways to make technical work open to review. These habits matter whether I work independently or join a development team in the future.

## 2. Technical integration: what clean text really means

Preprocessing taught me that removing more text is not always an improvement. URLs, HTML fragments, missing fields and duplicate articles can distort an analysis, yet capital letters, dates, numbers and the original wording still matter to named-entity recognition and dependency parsing. I therefore see the value of keeping different representations of an article for different tasks, rather than forcing every module to use one aggressively cleaned string. Tokenization, stop words and lemmatization help organize vocabulary; spaCy's POS and dependency labels offer another view of sentence structure, but neither should be mistaken for perfect understanding.

The strongest methodological lesson was about **data leakage**. A model can look impressive for the wrong reason if the vocabulary is learned from articles that later appear in the test set. In NewsBot, predictive TF-IDF belongs inside the training folds, while the final holdout stays separate. Comparing a dummy baseline, Naive Bayes, Logistic Regression and Linear SVM then becomes a meaningful experiment rather than simply choosing whichever score looks best. Working within Colab-style computing limits also showed me why shared spaCy processing, sparse features and controlled text lengths are practical design decisions.

## 3. Business value and the meaning of a good result

The recorded BBC experiment retained **1,440** articles after removing exact duplicates. Its Linear SVM classified **277 of 288** held-out articles correctly: **96.18% accuracy** and **0.9605 macro-F1**. Those numbers are satisfying, but the confusion matrix changed how I interpret success. Eleven articles were still assigned to the wrong category, and entertainment had the weakest class F1, approximately **0.9515**. I learned to look for the cases behind the average, because an editorial team would experience the individual routing mistakes rather than an abstract percentage.

The other modules taught me similar caution. VADER captures word-level tone, not factual truth or the writer's opinion. An entity pair appearing together in a story is not proof of a relationship, and names such as 'Blair' and 'Tony Blair' can represent the same person under different forms. NewsBot can assist article triage and media research, but it should support decisions that people can check, not replace editorial judgment.

## 4. Integration, debugging, and accountability

Putting the modules together helped me recognize the difference between a convincing demonstration and a trustworthy evaluation. The fictional technology, football and politics articles show how the full pipeline responds to new text. They do not prove accuracy. That requires labeled articles held out from training, per-category scores, error analysis and a reproducible record of the run. I also learned why passing software tests is not the same as measuring a model: tests can confirm that code paths work, while held-out evaluation asks whether the predictions are actually useful.

Reviewing the GitHub Actions evidence added another lesson. An execution can successfully process the BBC data and still have trouble publishing files if the repository changes during the run. Seeing an error annotation alongside an overall green status showed me that I should read individual step logs, not rely on a badge alone. The resulting workflow, figures, model artifact and report make the results easier for another person to inspect. For me, good documentation is part of the engineering work, not something added only at the end.

## 5. What I would improve next

My next experiment would use newer, appropriately licensed articles from several publishers. The BBC material comes from 2004-2005, so even strong results on its own holdout cannot show how NewsBot handles today's vocabulary, changing events or different editorial styles. I would compare macro-F1 and category-specific recall across sources, inspect incorrect predictions, and build a human-review option for ambiguous stories. I would also test whether confidence calibration helps decide when the system should abstain rather than force a category.

For information extraction, I would work on resolving entity aliases and evaluating recognition mistakes. For sentiment, I would compare VADER with methods that better handle quotations, context and irony. I would prioritize changes supported by measurable errors rather than adding features simply to make the project look more complex.

## 6. Professional growth and what I take forward

NewsBot changed how I think about an AI project being 'finished.' A notebook that runs is a starting point; a credible project explains where the data came from, why a model was selected, what its mistakes look like, and whether another person can reproduce the result. I have gained a clearer understanding of how preprocessing, vectorization, grammatical analysis, sentiment, classification and NER complement one another, and why each output needs careful interpretation. Just as importantly, I am learning to communicate those details without exaggerating what the model knows.

Preparing this project for GitHub and a short video also pushed me to think about my audience. A professor or future employer should be able to find the code, follow the methodology and see the evidence without guessing where the results are. AI-assisted tools can help explain syntax and debug implementation issues, but I remain responsible for checking the outputs, understanding the choices and making my reflection genuinely my own. The lesson I want to carry forward is that technical ambition matters most when it is matched by transparency, patience, and a willingness to investigate mistakes.

---

**Final check:** Confirm the experiences reflect your actual learning. The course also requires a two-page PDF and instructor approval for the dataset and submission arrangement. [PDF reflection](NewsBot_Reflection_Solo.pdf).
