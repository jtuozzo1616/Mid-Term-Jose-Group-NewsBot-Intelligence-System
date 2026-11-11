# Architecture, quality policy and limitations

**Purpose.** NewsBot 2.0 demonstrates a layered news NLP platform and a realistic source-attribution policy, rather than an unsupervised content publishing bot.

## System contracts

- `Article`: safe ID, normalized title/body, source metadata, optional category/language, SHA-256 content digest.
- `Retriever`: optional embedding search (opt-in), otherwise sparse TF-IDF over a constrained multilingual lexicon pivot; returns stable IDs and lexical/embedding score, **not a probability**.
- `Classifier`: trained using fully labeled local documents, optional trusted BBC midterm joblib. New inference is never marketed as validated 2026 accuracy.
- `Analyzer`: NMF topics, extractive summary, VADER or weak lexicon sentiment, optional spaCy NER with honest fallback, template-enhanced headlines.
- `Conversation`: user's query -> retrieval -> quoted sentences -> original article IDs; abstain on no or low retrieval evidence; explicitly resolve certain follow-up questions to prior source title.
- `API`: request schema limits and no internet fetching; persistent in-process demo data; route `/health`, `/overview`, `/articles`, `/search`, `/chat`, `/topics`.
- `Streamlit`: session-scoped engine, optional local user data import, real source attribution and charting.

## Why the design is robust

The evidence policy separates four incompatible concepts: topic category, linguistic tone, text similarity, and factual correctness. None is silently converted into the others. All generated answer passages are direct quotations or excerpts from known input articles. If a query cannot be grounded, the app declines to synthesize unsupported facts. A curated bilingual pivot helps basic cross-language discovery when no weights are installed. A user can opt into trained multilingual sentence embeddings, but the default mode never pretends it has downloaded or used one.

## Failure modes and threat boundaries

| Risk | Current safeguard | Production improvement |
|---|---|---|
| Hallucinated answer | Only verbatim source sentences with IDs and abstention | Human fact checking and answerability benchmark |
| Prompt injection in article body | No instructions executed from external text, no generative model | Sandboxed LLM and contextual injection audit if LLM added |
| Dataset / temporal drift | Historical BBC scores isolated from new data | Publisher- and year-stratified external holdout |
| Overconfident probabilities | Uncalibrated classifier scores explicitly labeled | Calibrated model plus out-of-domain detection, frozen test set |
| Language confusion | `und` for low-signal detection, lexicon limits described | Validated language ID and multidomain multilingual eval |
| Data provenance | SHA-256 content digest, source and synthetic markers | Signed ingestion manifest, audit trails, publisher licenses |
| Untrusted pickle | Only trusted local joblib explicit path | Signed model artifacts, checksum pinning |
| Denial of service | Body cap, file cap, bounded corpus & query | Auth, quotas, containers and memory profile |
| User content privacy | No silent remote API and session-scoped UI state | Access logs, encryption, retention and deletion policy |
| Unlicensed articles | Includes only authored synthetic samples | Data licensing and opt-in real source feeds |

## Evaluation protocol

Use time-separated and publisher-separated independent examples to test a future real dataset. Freeze all model selection on the training partition and calibrate abstention thresholds on validation data only. Separately report (a) category macro-F1, (b) topic coherence/stability, (c) sentiment agreement with human annotations, (d) cross-language retrieval MRR/Recall@K, (e) summarization faithfulness and coverage, and (f) conversational answer citation precision and abstention correctness. Report per-language metrics and inference latency on CPU. Never select thresholds on the final held-out sample and re-report them as independent.

## Scope of provided evidence

The included `artifacts/research_results.json` is a controlled functional research demonstration. The original midterm historical BBC evaluation remains independently published in the parent repository and is not recomputed here. Default installation does not contain an abstractive LLM, installed multilingual embeddings or an Argos translation pack. An optional frontend source is included but browser-side acceptance tests are not included in this release.
