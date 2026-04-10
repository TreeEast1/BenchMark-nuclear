# FermiBench Analysis

## Publicly observable dataset structure

Atomic Canyon publishes FermiBench on Hugging Face as a gated dataset with a BEIR-style layout:

- `corpus.jsonl`
- `queries.jsonl`
- `qrels/`
- `LICENSE`
- `README.md`

Although the full files require dataset access, the public dataset card and model card expose enough information to recover the benchmark design logic:

- 117,755 nuclear-domain documents in the corpus
- 300 benchmark queries
- 7,736 relevance judgments
- retrieval evaluation reported with `nDCG@10`, `MAP@100`, `Recall@100`, and related BEIR-style metrics

Primary sources:

- Hugging Face dataset page: <https://huggingface.co/datasets/atomic-canyon/FermiBench>
- Hugging Face file tree: <https://huggingface.co/datasets/atomic-canyon/FermiBench/tree/main>
- Hugging Face model card for `fermi-1024`: <https://huggingface.co/atomic-canyon/fermi-1024>

## Organization logic

### `corpus.jsonl`

The corpus follows the familiar BEIR convention: one JSON object per document, typically with `_id`, `title`, and `text`, plus optional metadata. FermiBench is notable because its source material is not short web snippets. It is dominated by long-form nuclear PDFs and technical reports, including plant, regulator, and standards documents.

The design implication is important: FermiBench appears to preserve report-level semantic context instead of flattening everything into tiny chunks. That choice is appropriate for nuclear engineering because:

- section references depend on the surrounding document context
- the same acronym can mean different things depending on plant system or accident phase
- compliance interpretation often spans multiple sections rather than one paragraph

For NuSafetyBench, this strongly suggests keeping document-level records in `corpus.jsonl`, while deriving chunk-level retrieval units only as an additional index, not as the canonical source artifact.

### `queries.jsonl`

The public card states that the 300 queries were crafted to represent realistic information needs in nuclear operations and engineering. This points to a retrieval-oriented benchmark, not a simple factoid dataset. Queries likely target:

- component and system definitions
- procedures or operating limits
- accident-condition information needs
- cross-document technical lookups

The fact that Atomic Canyon reports retrieval metrics instead of generation metrics also supports the interpretation that `queries.jsonl` is designed for dense or sparse retrieval benchmarking first.

### `qrels`

FermiBench uses BEIR-style relevance judgments. In this format, each query is associated with one or more document IDs and graded relevance labels. The existence of 7,736 qrels across 300 queries implies multi-document relevance per query, which is expected for nuclear documentation where the same operational question can be answered by:

- a design-basis section
- a system description chapter
- an operating procedure appendix
- a safety-analysis report table or figure

This is a better fit for nuclear work than single-answer QA because it evaluates whether a retrieval system can surface the right technical evidence set.

## How FermiBench handles long nuclear PDFs

The visible benchmark design suggests a retrieval-first strategy rather than a generation-first one:

1. Preserve long technical documents as the benchmark source of truth.
2. Encode them with a domain-specific retriever (`fermi-1024`) trained for long-context semantic search.
3. Evaluate ranking quality with BEIR metrics against expert-defined qrels.

That is a pragmatic solution to nuclear PDF complexity:

- PDFs often contain OCR noise, headers, footers, tables, and appendices.
- Many important answers live in dense prose, not in FAQs.
- The benchmark can evaluate retrieval quality before introducing an LLM generator.

In other words, FermiBench isolates the document-access problem: can a system find the right evidence in a large, noisy nuclear corpus?

## What dimensions FermiBench measures

Based on the public benchmark artifacts and metrics, FermiBench most clearly measures:

1. Domain-specific semantic retrieval
2. Multi-document evidence discovery
3. Terminology-sensitive matching in nuclear engineering language
4. Long-document relevance ranking

It does **not** appear to natively measure:

- full compliance auditing
- multi-turn accident management
- physical plausibility of generated recommendations
- chain-of-thought consistency over sequential operator updates

That gap is exactly where NuSafetyBench can differentiate.

## Likely gold-standard construction process

Atomic Canyon states that FermiBench uses expert-labeled relevance judgments. For a domain like nuclear engineering, a defensible gold-standard workflow is almost certainly close to the following:

1. Assemble a curated document corpus from nuclear technical sources.
2. Write realistic engineering or operations queries.
3. Retrieve candidate documents with baseline search systems.
4. Ask domain experts to judge which documents are relevant to each query.
5. Convert those judgments into qrels for benchmark scoring.

The most important part is not just the presence of labels, but the expert nature of the judges. Nuclear retrieval quality is highly sensitive to subtle distinctions:

- design requirement versus operational recommendation
- generic industry guidance versus plant-specific procedure
- normal operation versus accident mitigation

That means expert adjudication is not optional. It is the only way to create a benchmark whose relevance labels are technically trustworthy.

## Design lessons for NuSafetyBench

FermiBench provides four strong lessons:

1. Start with retrieval discipline before attempting grand safety claims.
2. Preserve document provenance and long-form context.
3. Use expert labeling rather than crowd annotation.
4. Benchmark on realistic information needs, not trivia.

NuSafetyBench should keep those strengths but extend the target from retrieval accuracy to safety-critical dialogue performance.

