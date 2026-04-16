# SST Autonomous Driving — Test 3 (Enhanced Scene Semantics + Decision Constraints)

## Overview

This experiment evaluates the SST-based decision system after introducing:
- Structured hazard metadata in scene JSON (severity, proximity, path status, urgency)
- Stronger decision constraints in the action prompt

The goal was to improve:
- Action escalation
- Safety alignment
- Context-aware decision behavior

---

## System Behavior Summary

### Key Improvements Over Previous Versions

#### 1. Emergence of Structural Actions (Major Improvement)

- The model now uses:
  - `merge_left` in construction scenarios
- This indicates:
  - transition from reactive → proactive behavior

Example:
- Construction frame 02: `maintain_speed → merge_left`

---

#### 2. Correct STOP Behavior in Crash Scenario (Critical Improvement)

- First occurrence of `stop` in high-risk situation:
  - Accident frame 04 (blocked lane)

This confirms:
> The system now recognizes fully blocked paths and escalates appropriately

---

#### 3. Improved Action Diversity

Compared to V2:
- Reduced repetition of `slow_down`
- More context-sensitive decisions:
  - `merge_left`
  - `stop`
  - `slow_down`
  - `maintain_speed`

---

#### 4. Strong Pedestrian Behavior Maintained

- Continues to output `stop` for:
  - crossing
  - conflict scenarios
- Correctly prioritizes pedestrian safety over traffic signals

---

## Remaining Weaknesses

### 1. Inconsistent Escalation in High-Risk Scenarios

While improved, escalation is still incomplete.

Examples:

- Collision event (frame 03):
  - `slow_down` instead of `stop`

- Post-collision (frame 05):
  - `maintain_speed` despite debris and risk

---

### 2. Unsafe Use of `maintain_speed`

Still appears in risky contexts:

- Construction frame 05
- Crash frame 02
- Crash frame 05

Indicates:
> The model still defaults to motion continuity in uncertain scenarios

---

### 3. Partial Risk Awareness but Weak Action Mapping

The system:
- correctly describes hazards
- correctly identifies severity

BUT:
- does not always map severity → appropriate action

---

### 4. Overconfidence Persists

- Many high-risk frames still labeled `"confidence": "high"`
- Confidence not fully aligned with uncertainty

---

## Behavior Trends

### Construction Scenario

Pattern:
slow → merge → slow → slow → maintain


Improvements:
- introduction of merging behavior

Remaining issue:
- failure to slow/stop in final high-risk frame

---

### Crash Scenario

Pattern:
maintain → maintain → slow → STOP → maintain → slow → slow


Improvements:
- first STOP appears

Remaining issue:
- STOP not consistently applied in critical frames

---

### Pedestrian Scenario

Pattern:
stop → stop → stop → stop → slow


Status:
- strong and stable
- no regression

---

## Key Insight

Adding structured scene semantics significantly improved:
- action diversity
- hazard recognition
- emergence of correct stopping behavior

However:

> The system still under-applies STOP actions and inconsistently maps high-risk situations to appropriate decisions.

---

## Conclusion

The system shows clear progression:

- V1 → reasoning only
- V2 → constrained decisions
- V3 → semantically-informed decision making

Remaining challenge:

> Achieving consistent and reliable action escalation in high-risk scenarios

---

## Next Step

Further refine decision policy to:

- enforce STOP in:
  - collision events
  - blocked paths
  - immediate hazards

- reduce use of `maintain_speed` in non-clear scenarios

- align confidence with uncertainty


