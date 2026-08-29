# Handoff Notes

Read `README.md` first for the research framing (SST patent connection, why
the pipeline is shaped the way it is, and the V1-V4 iteration history). This
doc is the practical guide for "how do I run this and what's actually done."

---

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You need [Ollama](https://ollama.com) running locally with two models pulled:

```bash
ollama pull mistral:instruct
ollama pull qwen2.5vl:7b
```

(`mistral:instruct` does the text reasoning/decision steps, `qwen2.5vl:7b` does
scene description from images. Both are configured in `src/config.py`. Swap
either for a different local model name if you'd rather use something else.)

Run everything from the repo root (scripts use relative paths like
`data/...`, `prompts/...`):

```bash
# full video -> frames -> vision -> reasoning -> decision pipeline
PYTHONPATH=src python3 src/run_pipeline.py data/raw/sample_construction_drive.mp4

# reasoning/decision only, against hand-authored scene JSON (no vision model needed)
PYTHONPATH=src python3 src/run_scenario.py
```

`run_pipeline.py` prints Observation / Safety Self-Talk / Action / Explanation
per frame and logs full detail (scene.json, reasoning.txt, action.json,
summary.json) under `logs/pipeline_video_test/<video_name>/`.

---

## What's already implemented

- **`extract_frames.py`** - samples ~10 evenly-spaced frames from a video with
  opencv.
- **`vision_to_text.py`** - vision-model call - sends the frame to `qwen2.5vl:7b` via Ollama with
  `prompts/vision_scene_prompt.txt`, gets back the same structured scene JSON
  schema documented in `data/README.md` and an `observation` field for a
  plain-language summary
- **`sst_reasoning.py`** - takes an optional `history` list (prior frames'
  reasoning text). `run_pipeline.py` passes a rolling window
  (`HISTORY_WINDOW` in `config.py`, default 3) so reasoning can build evidence
  across frames instead of re-deriving it each time. `run_scenario.py`
  doesn't pass history (single-frame scenes), so it's unaffected.
- **`run_pipeline.py`** - orchestrator tying the above together. Doesn't
  replace `run_scenario.py`, which is still the process for iterating on
  reasoning/decision prompts without a vision call in the loop.
- **`data/raw/sample_construction_drive.mp4`** - a synthetic test clip
  stitched from `data/frames/construction_test/` so `run_pipeline.py` has 
  a real video to run against. It's 5 source images held for a few frames each, 
  not an actual dashcam clip - swap in a real one for full testing. 
  A run against it is logged at `logs/pipeline_video_test/sample_construction_drive/` 
  and shows the escalation pattern working: `maintain_speed` through the early
  low-severity construction frames, then `slow_down` once a stopped vehicle
  blocks the lane.

## Next Steps

- **No retry/validation on vision output.** `vision_to_text.py` raises if the
  model doesn't return valid JSON. `qwen2.5vl:7b` was reliable in testing but
  isn't guaranteed to always emit strict JSON - might be worth adding a retry 
  with reprompt if it comes up.
- **History is raw reasoning text, not summarized.** Fine for a 10-frame demo;
  would need condensing (or a shorter window) for longer sequences so the
  prompt doesn't grow too larger.
- **`communication_modes.py`** (audience-specific explanations, listed in the
  original `src/README.md` plan) still doesn't exist. Out of scope here -
  Action + Explanation from `decision_extraction.py` covers the core loop.
- Everything already listed in `README.md` under "What Still Needs To Be
  Done" is still true: STOP-rule tuning, an evaluation framework against
  human actions, confidence calibration. That list didn't change as I only
  added the vision/temporal side.

## Where to look

- `README.md` - research framing and the V1-V4 iteration history/results
- `logs/0N_full_test/analysis.md` - per-version writeups of what changed and
  what the model actually did (only reasoning+decision, pre-vision)
- `logs/pipeline_video_test/` - the new video-based end-to-end run
- `src/README.md` - script-by-script description, kept in sync with this pass
- `data/README.md` - scene JSON schema
