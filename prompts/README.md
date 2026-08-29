# Prompt Design Philosophy

This directory contains prompt templates used for SST-based reasoning and communication.

---

## SST Prompt Goals

- Explicit scene understanding
- Clear risk identification
- Enumeration of possible actions
- Selection of a justified final action

---

## Prompt Types

- `sst_reasoning_base_prompt.txt`
  - Core self-talk reasoning prompt. Takes the current scene, and optionally
    prior frames' reasoning, so it can reason about an evolving situation
    instead of one frame at a time

- `vision_scene_prompt.txt`
  - Instructs the vision model to turn an image into the structured scene
    JSON schema in `data/README.md`

Audience-specific prompts (a human-friendly explanation, a machine-facing
intent message) were planned but aren't built - see `communication_modes.py`
in root `HANDOFF.md`.

---

## Notes

- Prompts are structured and deterministic
- Prompts are versioned and logged
- Reasoning clarity is prioritized over verbosity
