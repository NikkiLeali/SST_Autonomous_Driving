# Source Code Overview

This directory contains the core Python scripts for the project pipeline. Each script performs a single, well-defined step.

---

## Pipeline Order

1. `extract_frames.py`
2. `vision_to_text.py`
3. `sst_reasoning.py`
4. `decision_extraction.py`

`run_pipeline.py` wires steps 1-4 together for a real video. `run_scenario.py` is
a separate, lighter-weight harness - originally 3-4 only, against hand-authored
scene JSON in `data/test_scenes/` (that's what the versioned `logs/0N_full_test`
runs came from), since extended to also run 2-4 directly against a folder of
images. See root `HANDOFF.md` for current status.

`communication_modes.py` (audience-specific explanations) was in the original
plan but isn't built - out of scope for the handoff, see root `HANDOFF.md`.

---

## Script Descriptions

- `extract_frames.py`
  - Samples ~N evenly-spaced frames from a driving video (opencv)

- `vision_to_text.py`
  - Calls a local vision-language model via Ollama (`qwen2.5vl:7b`) and returns
    a structured scene JSON matching the schema in `data/README.md`

- `sst_reasoning.py`
  - Applies Self-Talk (SST) prompts to reason about the scene. Takes an
    optional `history` list of prior frames' reasoning so it can build on
    earlier uncertainty instead of treating each frame independently

- `decision_extraction.py`
  - Converts reasoning outputs into structured driving actions

- `run_pipeline.py`
  - Orchestrates the full video -> frames -> vision -> reasoning -> decision
    path, carrying a rolling reasoning history (`HISTORY_WINDOW` in
    `config.py`) across frames, and prints/logs Observation / Safety
    Self-Talk / Action / Explanation per frame

- `run_scenario.py`
  - Batch-runs hand-authored scene JSON through reasoning + decision (used
    for the versioned experiments in `logs/`), or a folder of images through
    vision + reasoning + decision

---

## Design Principles

- Modular scripts
- No real-time assumptions
- Deterministic, logged outputs
- Clear input/output boundaries
