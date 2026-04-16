# SST Autonomous Driving — Test 4 (Scene + Structured Reasoning + Constrained Decision)

## Overview

This experiment evaluates the full SST pipeline with:
- structured scene inputs (hazard severity, proximity, path status)
- structured SST reasoning
- scene-aware, constraint-based decision-making

This represents the **intended final architecture**.

---

## System Behavior Summary

### Key Improvements

#### 1. Reliable STOP Behavior (Major Improvement)
- STOP is now consistently triggered in:
  - collision events
  - blocked lane scenarios
  - immediate hazards

This resolves the primary failure seen in earlier versions.

---

#### 2. Correct Action Escalation

Observed pattern:
`maintain → slow → STOP`


- Actions now escalate appropriately with increasing risk
- Strong alignment between:
  - hazard severity
  - path status
  - final decision

---

#### 3. Emergence of Structured Actions

- Construction scenarios now include:
  - `merge_left`
  - `stop` in conflict cases

Indicates transition from:
> reactive → proactive decision-making

---

#### 4. Strong Scene → Decision Alignment

- Decisions now directly reflect structured fields:
  - `hazard_severity`
  - `hazard_proximity`
  - `path_status`

This confirms:
> structured inputs successfully guide LLM behavior

---

#### 5. Stable Pedestrian Safety

- Maintains correct STOP behavior across all pedestrian scenarios
- Properly handles signal conflicts (green light vs pedestrian)

---

## Remaining Weaknesses

#### 1. Early-Stage Underreaction

- Some early hazard frames still produce:
  - `maintain_speed` instead of `slow_down`

Indicates:
> delayed response to emerging risk

---

#### 2. Residual Overuse of `maintain_speed`

- Appears in scenarios where:
  - hazards are present but not yet critical

Needs refinement:
> maintain_speed should only occur when path is fully clear

---

#### 3. Confidence Calibration

- High confidence still appears in uncertain conditions
- Confidence not yet aligned with true risk level

---

## Behavior Patterns

### Construction
`slow → merge → slow → merge → stop`


### Crash
`maintain → slow → STOP → STOP → STOP → slow`

### Pedestrian
`stop → stop → stop → stop → slow`


---

## Key Insight

> Reliable safety behavior emerges only when structured scene semantics and explicit decision constraints are combined with SST reasoning.

---

## Conclusion

V4 demonstrates:

- consistent safety-aligned behavior  
- correct action escalation in high-risk scenarios  
- strong integration of reasoning and structured decision constraints  

Remaining work focuses on:
- earlier hazard response  
- reducing unnecessary `maintain_speed`  
- improving confidence calibration  

---

## TL;DR

- V4 achieves consistent STOP behavior in critical scenarios  
- Scene structure + reasoning + constraints = correct decisions  
- Remaining issues are minor (early response + confidence)

