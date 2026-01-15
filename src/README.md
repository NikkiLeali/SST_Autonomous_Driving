# Source Code Overview

This directory contains the core Python scripts for the project pipeline. Each script performs a single, well-defined step.

---

## Pipeline Order (experimental)

1. `extract_frames.py`
2. `vision_to_text.py`
3. `sst_reasoning.py`
4. `decision_extraction.py`
5. `communication_modes.py`

---

## Script Descriptions (experimental)

- `extract_frames.py`
  - Extracts representative frames from driving videos

- `vision_to_text.py`
  - Converts frames into structured scene descriptions

- `sst_reasoning.py`
  - Applies Self-Talk (SST) prompts to reason about the scene

- `decision_extraction.py`
  - Converts reasoning outputs into structured driving actions

- `communication_modes.py`
  - Generates audience-specific explanations and intent messages

---

## Design Principles

- Modular scripts
- No real-time assumptions
- Deterministic, logged outputs
- Clear input/output boundaries
