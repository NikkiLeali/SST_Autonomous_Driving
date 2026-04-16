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

## What Still Needs To Be Done

### 1. Decision Layer (Final Tuning)
- Strengthen STOP enforcement rules
- Improve mapping:
  hazard_severity → action
- Reduce maintain_speed usage when hazards are present
- Improve early-stage hazard response (pre-escalation behavior)

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
  - reliable STOP behavior in high-risk scenarios
  - consistent emergence of structured actions (STOP, MERGE)
- Still needs:
  - consistent STOP in high-risk cases
  - vision-based perception

