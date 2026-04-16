# SST Autonomous Driving — Project Summary

## Connection to SST Patent

This project directly implements the core idea of the SST (Safety Self-Talk) patent:
- Drivers perform internal “self-talk” before acting
- This reasoning influences safe driving decisions
- LLMs are used to simulate this reasoning process

Patent principle:
“Safety self-talk is the main initiative of subsequent safety actions.”

## System Interpretation of SST

The system operationalizes SST as:
`Scene (structured state) → Self-Talk Reasoning (LLM) → Decision (LLM with constraints)`

Key extension:
- Reasoning is separated from decision
- Structured scene data is preserved for safety enforcement

This results in:
- explainable decisions
- interpretable reasoning
- safety-aware action selection

---

## Methods

### Current Pipeline

`Scene JSON (manual perception) → SST Reasoning (LLM) → Decision Extraction (LLM + rules) → Structured Output`

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

### Observed Behavior

Strengths:
- Strong pedestrian safety (consistent STOP)
- Context-aware decisions
- Improved action diversity (merge, stop)
- Reasoning aligns with scene inputs

Weaknesses:
- STOP still inconsistent in crash scenarios
- Occasional unsafe maintain_speed
- Weak risk → action escalation
- Confidence overestimated

### Key Insight

Structured scene representations significantly improve decision quality, but:
LLMs require explicit constraints to reliably escalate actions in high-risk scenarios.

---

## What Still Needs To Be Done

### 1. Decision Layer (Final Tuning)
- Strengthen STOP enforcement rules
- Improve mapping:
  hazard_severity → action

### 2. Vision → Scene Pipeline
Replace manual JSON with:
`image → detection/caption → structured JSON`

### 3. Temporal Reasoning
Extend from single frame → multi-frame reasoning

### 4. Evaluation Framework
- Compare against human actions
- Measure correctness and safety

### 5. Confidence Calibration
- Multi-run agreement
- uncertainty estimation

---

## TL;DR

- Implemented SST (self-talk) using LLMs for driving decisions
- Built pipeline: scene → reasoning → decision
- Major improvements came from:
  - structured scene inputs
  - decision constraints
- System now shows:
  - strong reasoning
  - good pedestrian safety
  - emerging correct actions (STOP, MERGE)
- Still needs:
  - consistent STOP in high-risk cases
  - vision-based perception

