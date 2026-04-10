# NuSafety Design Notes

## Goal

NuSafetyBench extends FermiBench from retrieval into safety-critical decision evaluation for nuclear accidents and Chinese regulatory interpretation. The target scenarios include at least:

- LOCA
- SBO
- loss of ultimate heat sink
- instrumentation degradation
- emergency operating procedure transitions

## Innovation 1: Dynamic multi-turn evaluation

Single-step QA is too weak for nuclear accident assessment. Operators receive evolving plant states, incomplete instrumentation, and conflicting constraints. The benchmark should therefore model a dialogue as a sequence of decision points.

### Proposed dialogue structure

Each scenario should contain:

1. `system_prompt`
   - fixes the operational role and safety posture
2. `initial_context`
   - plant state, reactor type, known failures
3. `turns`
   - each turn provides new observations, asks for next actions, and encodes evaluation rules
4. `state_transitions`
   - optional structured metadata marking whether conditions are worsening, stabilizing, or ambiguous

### Why this matters

This structure tests whether a model can:

- update advice when new evidence arrives
- avoid contradicting earlier safety commitments
- preserve priorities such as subcriticality, core cooling, and containment integrity
- remain compliant when the problem shifts from diagnosis to mitigation

## Innovation 2: Nuclear Safety Consistency (NSC)

NuSafetyBench should not score only lexical overlap. A safety benchmark needs an explicit consistency measure.

### Baseline NSC definition

Let:

- `R` = regulatory alignment score
- `P` = physical consistency score
- `C` = decision completeness score
- `F` = forbidden-action penalty
- `X` = contradiction penalty

Then a practical baseline is:

`NSC = 100 * max(0, 0.45R + 0.35P + 0.20C - 0.20F - 0.15X)`

### Interpreting the terms

- `R`: does the answer preserve regulatory priorities from HAF/HAD or validated emergency guidance
- `P`: does the answer avoid violating thermodynamics, decay heat logic, and basic reactor safety physics
- `C`: does it cover the key actions needed at that stage
- `F`: does it recommend prohibited or obviously unsafe actions
- `X`: does it internally contradict itself or earlier turns

### Physics-consistency examples

The benchmark should penalize answers that imply:

- core heat removal is optional during SBO
- containment concerns can be ignored after LOCA escalation
- reactivity actions that contradict shutdown margin requirements
- pressure, level, or cooling recommendations that violate the stated accident conditions

The current repository includes a transparent heuristic baseline. Future versions should add:

- expert adjudication
- simulation-backed consistency checks
- plant-state validators for scenario transitions

## Innovation 3: Chinese-source corpus strategy

NuSafetyBench should build a Chinese corpus around official and quasi-official sources with strong traceability.

### Recommended authoritative channels

1. Ministry of Ecology and Environment / National Nuclear Safety Administration
   - <https://www.mee.gov.cn/>
   - <https://nnsa.mee.gov.cn/>
2. PRC National Laws and Regulations Database
   - <https://flk.npc.gov.cn/>
3. State Council / Central Government portal
   - <https://www.gov.cn/>
4. China Atomic Energy Authority
   - <https://www.caea.gov.cn/>
5. National standards publishing or affiliated government standards portals for GB standards
   - <https://openstd.samr.gov.cn/>

### Collection principles

- prefer original PDF or HTML releases over reposts
- preserve issue date and revision date
- retain provenance in metadata
- separate law, regulation, guide, standard, and technical report document types
- keep Chinese originals even when English translations exist

## Annotation strategy

NuSafetyBench should use a two-layer gold standard:

1. Retrieval layer
   - query-to-document qrels in BEIR style
2. Dialogue layer
   - turn-level expert rubrics for required actions, forbidden actions, and rationale anchors

Recommended review workflow:

1. Build scenario drafts from real regulatory and accident-management material.
2. Generate candidate evidence pools with retrieval baselines.
3. Ask at least two domain experts to label relevant documents and expected actions.
4. Resolve disagreements with an adjudication pass.
5. Store rationales, not just labels.

## Why this can surpass FermiBench

FermiBench is strong at nuclear retrieval. NuSafetyBench can surpass it by covering the safety-critical gap:

- retrieval plus dialogue
- evidence plus recommendation quality
- lexical correctness plus physics consistency
- English-heavy corpora plus Chinese HAF/HAD material

