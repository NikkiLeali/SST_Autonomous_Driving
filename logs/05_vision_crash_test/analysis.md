# SST Autonomous Driving — Vision Test (Crash Scenario)

## Overview
Tested vision model (Qwen2-VL) replacing manual scene JSON:
image → vision JSON → SST reasoning → decision

---

## Key Findings

### 1. Object Detection Works
- Correctly identifies:
  - vehicles
  - stopped cars
  - debris

### 2. Risk Interpretation Fails
- Collision scenes labeled:
  - hazard_severity = "medium"
  - path_status = "clear" or "partially_blocked"

Reality:
- lane is blocked
- hazard is critical

---

### 3. Impact on Decisions
- STOP delayed or missing
- maintain_speed appears in unsafe frames
- weak action escalation

---

## Root Cause
Vision model describes the scene but does NOT infer:
- hazard severity
- path blockage
- urgency

---

## Key Insight
Vision models produce descriptive outputs, not decision-aware representations.

---

## Next Steps
- Improve vision prompt to enforce hazard interpretation
- Add mapping layer:
  vision output → decision-aware JSON
- (Optional) add simple rules for collisions / blocked lanes

---

## TL;DR
- Vision detects objects
- Fails to infer driving risk  
- Problem = perception interpretation, not SST pipeline  
