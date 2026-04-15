# SST Autonomous Driving — Test 1 (Baseline)

## Overview
This experiment evaluates the baseline SST reasoning and decision pipeline using:
- Manual scene JSON inputs
- Local LLM (Mistral via Ollama)
- Unconstrained decision prompt

Note: the scenes are manually vision-to-text. Not currently automated. 

---

## System Behavior Summary

### Strengths

#### 1. Context-Aware Reasoning
- The system adapts behavior across different scenarios:
  - Construction → cautious
  - Crash → increased awareness
  - Pedestrian → strong safety behavior

#### 2. Strong Pedestrian Handling
- Correctly outputs `stop` in all critical pedestrian frames
- Overrides traffic signal when pedestrian is present
- Demonstrates human-like prioritization of safety

#### 3. Coherent and Logical Reasoning
- Reasoning aligns with input scene descriptions
- No hallucinated hazards or objects
- Intent explanations are clear and interpretable

#### 4. Conservative Bias
- Defaults to `slow_down` under uncertainty
- Avoids aggressive or risky behavior

---

### Weaknesses

#### 1. Failure to Escalate in High-Risk Scenarios (Critical)
- No `stop` actions in crash sequence
- Unsafe behavior in collision and blocked lane situations

Example:
- Collision event → `slow_down` instead of `stop`
- Blocked lane → `maintain_speed`

---

#### 2. Overuse of `maintain_speed`
- Appears in situations where caution is required
- Seen in both construction and crash scenarios

---

#### 3. Lack of Structural Actions
- No use of:
  - `merge_left`
  - `merge_right`
  - `yield`
- Indicates passive rather than strategic behavior

---

#### 4. Overconfident Outputs
- Frequent `"confidence": "high"` in dangerous situations
- Confidence not aligned with risk level

---

#### 5. Underreaction Pattern
- Actions do not escalate with increasing hazard severity

Pattern observed:
maintain → slow → slow → slow

Expected:
maintain → slow → STOP → STOP


---

## Key Insight

The system demonstrates strong reasoning capability but lacks:
- Decision escalation
- Safety-critical action enforcement

This suggests the need for:
> Explicit decision policy constraints in the action selection prompt

---

## Next Step

Introduce structured decision rules in the prompt to:
- Enforce STOP in high-risk situations
- Encourage action escalation
- Improve alignment between reasoning and action
