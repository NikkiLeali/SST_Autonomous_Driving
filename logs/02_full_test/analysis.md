# SST Autonomous Driving — Test 2 (Decision-Constrained Prompt)

## Overview
This experiment evaluates the SST reasoning and decision pipeline after introducing explicit decision constraints into the action selection prompt.

The goal of this update was to:
- Improve safety-aligned decision making
- Enforce action escalation in high-risk scenarios
- Better align reasoning with final actions

---

## System Behavior Summary

### Improvements Over Baseline

#### 1. Increased Use of Conservative Actions
- More frequent use of `slow_down` across scenarios
- Reduced overuse of `maintain_speed`
- Better alignment with uncertain or evolving situations

Example:
- Construction frame 01: `maintain_speed → slow_down`
- Crash frame 04: `maintain_speed → slow_down`

---

#### 2. Improved Behavior in Crash Scenario
- No longer uses `maintain_speed` in clearly unsafe blocked lane scenarios
- Demonstrates increased caution in most frames

However:
- Still does not escalate to `stop` in collision events

---

#### 3. Consistent Pedestrian Handling (Maintained Strength)
- All critical pedestrian frames still correctly output `stop`
- Correctly handles signal conflict (green light vs pedestrian)
- Demonstrates strong human-like safety prioritization

---

#### 4. More Balanced Confidence Levels
- Confidence reduced from mostly `high` → more `medium`
- Better reflects uncertainty in complex scenarios

---

### Remaining Weaknesses

#### 1. Still Fails to Escalate to STOP in Crash Scenario (Critical)
- No `stop` action in any crash frame
- Even during collision events and blocked lanes

Example:
- Collision event → `slow_down` instead of `stop`

---

#### 2. Occasional Unsafe Use of `maintain_speed`
- Appears in construction frame 04
- Appears in crash frame 06 (secondary collision risk)

This indicates:
> The model still defaults to maintaining motion instead of minimizing risk

---

#### 3. Lack of Structural Actions (Still Missing)
- No `merge_left`, `merge_right`, or `yield`
- System remains reactive rather than proactive

---

#### 4. Weak Risk Escalation Behavior

Observed pattern:
maintain → slow → slow → slow

Expected pattern:
maintain → slow → STOP → STOP


The system:
- Recognizes increasing danger
- But does not increase action severity accordingly

---

## Key Insight

Adding decision constraints improved:
- conservative behavior
- alignment with uncertainty

But did not fully solve:
- action escalation
- safety-critical stopping behavior

---

## Conclusion

The constrained decision prompt leads to:
- more cautious and stable behavior
- improved consistency across scenarios

However:
> The system still underreacts in high-risk scenarios and requires stronger enforcement of STOP actions.

---

## Next Step

Further refine the decision prompt to:
- strongly enforce STOP in collision scenarios
- discourage `maintain_speed` under uncertainty
- introduce clearer mapping between hazard severity and action choice
