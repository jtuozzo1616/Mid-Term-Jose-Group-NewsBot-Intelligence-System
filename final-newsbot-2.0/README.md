# NewsBot Intelligence System 2.0

**Final Project · ITAI 2373 · Houston Community College**  
**Project owner:** José Miguel Tuozzo Izaguirre  
**Status:** Executable, tested final-capstone prototype. Offline core verified; optional Streamlit frontend requires installation.  
**Lineage:** Builds upon the original [NewsBot Intelligence System midterm](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System), preserving its reported BBC model evaluation and eight NLP-module notebook.

> **Scientific honesty:** The 30 bundled news samples are **fictional synthetic classroom examples**. Their scores assess software behavior; they are not real-world production performance. The midterm's **96.18% BBC holdout accuracy / 0.9605 macro-F1** comes from a separate evaluation on 2004–2005 articles, not NewsBot 2.0.

## What can it do?

| Required module | Implementation | Interface / test evidence |
|---|---|---|
| **1. Advanced content analysis** | Optional reuse of midterm SVM, trainable local logistic classifier, NMF topic modeling, VADER/weak-lexicon sentiment, POS/NER via optional spaCy | Article Lab, Research Lab, `analysis.py`, synthetic stratified CV |
| **2. Language understanding & generation** | Extractive centroid/MMR summary with original sentence positions; explainable TF-IDF retrieval, template-based headline suggestions | Article Lab / Search / `retrieval.py` |
| **3. Multilingual intelligence** | Language heuristics, EN/ES/FR/DE constrained cross-language vocabulary pivot, optional multilingual SentenceTransformer embeddings, optional fully offline Argos translation | Search & Languages, `language.py` |
| **4. Conversational interface** | Multi-turn query reformulation, article-ID citations, grounded source excerpts, documented abstention when source support is insufficient | Grounded Chat, `chat.py` |
| **30-point web bonus candidate** | Five-tab Streamlit research dashboard with import, charts, article exploration, citations, chat and local evaluation | `app.py` |
| **20-point research bonus candidate** | 24 hand-authored retrieval probes, no-pivot ablation, synthetic CV, per-record content hashing and manifest | `run_research.py`, `artifacts/research_results.json` |

**Architecture:** `CSV/JSONL -> strict article validation -> normalization/provenance -> NLP analysis & NMF / optional classifier -> TF-IDF pivot or optional multilingual embeddings -> ranked source IDs -> extractive answer with citations -> Streamlit + FastAPI + CLI`.

## Quick start — no paid API required

Requires **Python 3.10–3.12 recommended**, although the tested code also passed locally on Python 3.13. All commands below are from the project root:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
python -m newsbot2.cli overview
python -m newsbot2.cli search --query "robot navigation sensors"
python -m newsbot2.cli search --retrieval-mode lsa --query "robot navigation sensors"
python -m newsbot2.cli ask --query "What did the AI chip researchers measure?"
python run_research.py
streamlit run app.py
```

If you only want the core functions, install `requirements-core.txt`. If using the API:

```bash
uvicorn newsbot2.api:app --reload
# API docs: http://127.0.0.1:8000/docs
curl -X POST http://127.0.0.1:8000/search -H "Content-Type: application/json" \
  -d '{"query":"robot cameras sensors", "k":3}'
```

If you run from the **original midterm repository**, the Streamlit interface automatically detects the **trusted local** `outputs/newsbot_classifier.joblib`. If it is absent, Streamlit trains a **fictional-demo-only classifier** from the bundled fixture and labels it as such. The standalone ZIP does not bundle BBC model weights or copyrighted training articles. Never load `.joblib` from unknown users: Python pickle-backed artifacts can execute code.

## Project structure

```text
NewsBot_Intelligence_2.0/
  app.py                      # Professional Streamlit bonus interface
  newsbot2/                   # Decoupled, typed NLP library
    schemas.py                # Article/provenance contracts
    io.py                     # Validated CSV and JSONL imports
    language.py               # Language hints, pivot, Argos translation integration
    analysis.py               # Topic modeling, classifier, summary, sentiment and NER
    retrieval.py              # Ranked retrieval and source excerpts
    chat.py                   # Source-grounded conversational logic
    engine.py                 # Unified application service
    evaluation.py             # Stratified CV and retrieval quality
    api.py                    # FastAPI service
    cli.py                    # Command-line workflows
  data/demo_news.jsonl        # 30 explicitly fictional stories, 4 languages
  tests/                     # Offline regression + API tests
  run_research.py             # Transparent bonus research extension
  artifacts/                  # Generated reproducibility evidence
  docs/                       # Methodology, project mapping and student documents
  .github/workflows/          # CI test workflow
```

## Load an instructor-approved real corpus

Supported `.csv` or `.jsonl` rows have `article_id,title,body` and optional `source,published_at,language,category,url,synthetic` fields. The importer rejects duplicate identifiers, unsupported schemes, malformed IDs and oversized files. Up to 3,000 articles or 8 MB, whichever is smaller.

**Do not publish copyrighted news article bodies without a license.** The original BBC midterm already documents its own data source and held-out evaluation. To reuse the trained midterm classifier, use:

```bash
python -m newsbot2.cli analyze --corpus data/demo_news.jsonl \
 --id demo-tech-1 --model outputs/newsbot_classifier.joblib
```

Important: applying that older SVM to a new or multilingual corpus is *inference*, not validation, and historical BBC category results should not be cited as accuracy for the new corpus.

## Optional genuinely semantic multilingual retrieval

The default `tfidf-pivot` retriever uses **transparent glossary assistance**, not a general-purpose translation engine or a sentence-meaning model. To enable learned cross-language embeddings, install the optional packages and explicitly load a multilingual model:

```bash
pip install -r requirements-advanced.txt
python -m newsbot2.cli search --query "robotica investigación" \
  --multilingual-model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

The initial model download requires internet access and storage; CPU inference works after its weights are cached. Optional [Argos Translate](https://github.com/argosopentech/argos-translate) requires *separately installed language packs*. In the default environment, translation returns `status=unavailable` rather than inventing output. Without spaCy English model, NER returns candidate phrases and labels them as approximate, not validated named entities.

## Evidence, evaluation and interpretation

1. **Inherited independent result:** Historical BBC 288-item holdout accuracy 0.9618 and macro-F1 0.9605 from the original midterm, across business / entertainment / politics / sport / tech. This is only **in-domain historic evaluation**; it doesn't measure this new implementation.
2. **New software tests:** `python -m pytest tests -q` tests input validation, provenance, evidence citation and abstention, topic modeling, multilingual pivot, API responses, conversation follow-ups and synthetic CV.
3. **New controlled research:** `run_research.py` computes 3-fold synthetic CV and compares MRR@3 and Recall@3 for baseline lexical matching versus a curated cross-language dictionary. Results are in `artifacts/research_results.json` and are **not** a cross-publisher benchmark.
4. **Model interpretability:** Sentiment explicitly states lexical bias, topic modeling reports approximate keywords, classification displays uncalibrated scores, and chat returns extractive article sentences with stable citations.
5. **Failure policy:** Unsupported input, missing model assets, no translation packs and weak source retrieval return explicit, safe statuses instead of fabricated fact claims.

## Responsible AI and deployment boundaries

- A production deployment needs authentication, abuse protection, rate limiting, HTTPS, persistence/backup, metrics, review workflows, deployment monitoring, and threat modeling. **This project does not claim those have been completed.**
- The tool is **not** a fact-checker; original source statements may be false or synthetic.
- Source excerpts and generated headlines require human editorial verification.
- No paid model calls, account secrets or news feeds are silently accessed. No remote URLs are fetched by the backend.
- Content input is bounded, normalized and assigned stable identifiers and SHA-256 hashes.
- NER and sentiment depend on language/model availability; translation is explicitly optional.
- Human written participation and team-member contribution attribution must be confirmed before final academic submission.

## Academic submission mapping

The project brief lists five separate deliverables; technical documentation and executive summary PDFs are in `docs/`. A **draft** reflective journal is provided for personal revision before submission. **Slides intentionally are not generated yet**, as requested: a matching presentation and slide-by-slide speech will be prepared when the student confirms the software is satisfactory.

**Naming note:** `JoseGroup` is a provisional group label borrowed from the former repository naming. Replace it if your Canvas group name differs. The separately downloaded detailed Canvas final-project instructions and web bonus requirements were not included with the assignment description; verify every rubric item against those source documents.

## References

- [Original NewsBot midterm repository](https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System)
- [scikit-learn — text feature extraction and decomposition](https://scikit-learn.org/stable/modules/feature_extraction.html)
- [Sentence Transformers — multilingual pretrained models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
- [Streamlit — chat components](https://docs.streamlit.io/develop/api-reference/chat)
- [Argos Translate — offline machine translation](https://argos-translate.readthedocs.io/en/stable/index.html)
- [FastAPI — API documentation](https://fastapi.tiangolo.com/)

**Version:** 2.0.0 · **Course:** ITAI 2373 · **Project owner:** José Miguel Tuozzo Izaguirre.

### CPU latent semantic alternative

The optional `--retrieval-mode lsa` projects TF-IDF features through truncated SVD and retrieves by cosine similarity in the lower-dimensional latent space. This is an in-corpus **LSA baseline**, not equivalent to pretrained cross-language semantic embeddings. No GPU or model download required.
