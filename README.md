# SST Autonomous Driving — Project Summary

## Motivation
Safety Self-Talk (SST) starts from the idea that safe driving decisions develop over time rather than from one isolated image. A driver may first notice brake lights, then see cones, and only later realize that a lane is blocked. The SST patent describes this as an evolving internal safety assessment in which new evidence changes both the interpretation of the scene and the action that follows. This project asks whether an LLM can serve as a limited reasoning layer in that process. It is not being used to control a real vehicle; instead, it receives scene information, reasons about hazards and uncertainty, and recommends a small set of high-level actions.

This fits into recent research work using language and vision-language models for autonomous driving. DriveGPT4, DriveVLM, DriveMLM, and Reason2Drive all connect visual driving information with explanation, reasoning, planning, or behavior selection. At the same time, reliability work such as DriveBench shows that VLMs can produce plausible driving answers without being fully grounded in the visual input. That concern is important for SST because a convincing explanation is not useful if the system misunderstood the scene.

## Connection to SST Patent

This project directly implements the core idea of the SST (Safety Self-Talk) patent:
- Drivers perform internal “self-talk” before acting
- This reasoning influences safe driving decisions
- LLMs are used to simulate this reasoning process

Patent principle:
“Safety self-talk is the main initiative of subsequent safety actions.”

## System Interpretation of SST

The system operationalizes SST as:
`Scene (structured state) -> Self-Talk Reasoning (LLM) -> Decision (LLM with constraints)`

Key extension:
- Reasoning is separated from decision
- Structured scene data is preserved for safety enforcement

This results in:
- explainable decisions
- interpretable reasoning
- safety-aware action selection

---

## Setup & Running

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires [Ollama](https://ollama.com) running locally with `mistral:instruct`
(reasoning/decision) and `qwen2.5vl:7b` (vision) pulled.

```bash
# full video -> frames -> vision -> reasoning -> decision pipeline
PYTHONPATH=src python3 src/run_pipeline.py data/raw/sample_construction_drive.mp4

# reasoning/decision only, against hand-authored scene JSON (no vision call)
PYTHONPATH=src python3 src/run_scenario.py
```

See **`HANDOFF.md`** for full setup detail, current project status, known
gaps, and next steps.

---

## Methods

### Current Pipeline

`Driving video → Frame extraction -> Vision model (scene JSON) -> SST Reasoning (LLM, evolving over frames) -> Decision Extraction (LLM + rules) -> Structured Output`

`run_scenario.py` still exists as a lighter-weight harness for iterating on
reasoning/decision prompts - originally against hand-authored scene JSON in
`data/test_scenes/` (what produced the V1-V4 results below), since extended
to also run vision + reasoning + decision directly against a folder of
images. See `HANDOFF.md` for the latest on that.

### Key Design Choices

- Structured scene representation (hazard severity, proximity, path status)
- Two-stage LLM pipeline:
  - reasoning (interpretation)
  - decision (enforced action selection)
- Constrained action space:
  maintain_speed, slow_down, stop, merge, yield

---

## Results / Iteration Summary

### Versions

| Version | Change | Outcome |
|--------|------|--------|
| V1 | Basic SST reasoning | Good reasoning, weak decisions |
| V2 | Decision constraints | More conservative behavior |
| V3 | Structured scene inputs | Emergence of STOP + MERGE |
| V4 | Structured reasoning + scene-aware decision | Consistent STOP in high-risk scenarios + improved action alignment |

### Observed Behavior

Strengths:
- Strong pedestrian safety (consistent STOP)
- Context-aware decisions
- Improved action diversity (merge, stop)
- Reasoning aligns with scene inputs
- Reliable STOP behavior in collision and blocked-lane scenarios (V4)
- Strong alignment between structured scene inputs and final decisions

Weaknesses:
- Early-stage underreaction (e.g., maintain_speed in emerging hazards)
- Occasional unsafe maintain_speed
- Weak risk → action escalation
- Confidence overestimated
- Maintain_speed still appears in some non-clear scenarios

### Key Insight

Structured scene representations and explicit decision constraints significantly improve decision quality.

Reliable safety behavior emerges when:
- scene semantics encode urgency (severity, proximity, path status)
- decision rules enforce action escalation

Reasoning alone is insufficient without structured grounding.

---

## Decision Behavior Progression

| Scenario | V1 | V3 | V4 |
|--------|----|----|----|
| Construction | maintain | merge appears | merge + stop correct |
| Crash | slow only | partial STOP | consistent STOP |
| Pedestrian | correct | correct | correct |

---

## Quick Summary

- Implemented SST (self-talk) using LLMs for driving decisions
- Built pipeline: video -> frames -> vision -> reasoning -> decision
- Major improvements came from:
  - structured scene inputs
  - decision constraints
- System now shows:
  - strong reasoning
  - reliable STOP behavior in high-risk scenarios
  - consistent emergence of structured actions (STOP, MERGE)

Current status, known gaps, and next steps: see **`HANDOFF.md`**.

