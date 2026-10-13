# Dataset approval request — SEND BEFORE USING KAGGLE DATA

**Subject: ITAI 2373 NewsBot Midterm — BBC News Dataset Approval Request**

Dear Professor,

I request approval to use the **BBC News Classification** dataset for the NewsBot Intelligence System midterm assignment.

- **Kaggle page:** https://www.kaggle.com/competitions/learn-ai-bbc/data
- **File:** `BBC News Train.csv`, the 1,490 **labeled** training articles from the competition. We will not treat the unlabeled 736-row competition test file as labeled evaluation data.
- **Categories (five):** business, entertainment, politics, sport, tech.
- **Format:** full-length English-language historical news articles, article ID, topical label.
- **Suitability:** exceeds the 500-article / four-category minimum, stays under the 2,000-article ceiling, supports TF-IDF, POS/dependency parsing, VADER, multi-class supervised learning and NER, and runs on Google Colab Free.
- **Plan:** use an internal stratified train/holdout split, five-fold CV limited to training, compare three classifier families plus dummy baseline, preserve original texts for entities and syntax, document domain bias and model errors.

**Five representative records** (title, class, and identifier from a publicly accessible CSV copy of the BBC competition training file; please cross-check the final authorized Kaggle download before sending):

| ArticleId | Category | Original headline / article opening |
|---|---|---|
| 1833 | business | Worldcom ex-boss launches defence |
| 1976 | tech | Lifestyle governs mobile choice |
| 1582 | politics | Howard 'truanted to play snooker' |
| 651 | sport | Wales silent on Grand Slam talk |
| 1797 | entertainment | French honour for director Parker |

These five records demonstrate substantive news text, the topical span of the five labels, and how the proposed source suits the requirements. Confirm the IDs/titles/categories against the approved Kaggle CSV before emailing the professor. Publicly inspected read-only mirror: https://raw.githubusercontent.com/alvinrach/learn-ai-bbc/main/BBC%20News%20Train.csv .

Would you approve this dataset for the NewsBot midterm? Please advise if you require a different source or additional conditions.

Sincerely,  
José Miguel Tuozzo Izaguirre  
Student: José Miguel Tuozzo Izaguirre (individual submission; separate solo approval requested)

**DO NOT SEND UNTIL THE 5 RECORDS HAVE BEEN CONFIRMED AGAINST THE OFFICIAL KAGGLE CSV AND INSTRUCTOR APPROVAL FOR INDIVIDUAL WORK IS REQUESTED.**
