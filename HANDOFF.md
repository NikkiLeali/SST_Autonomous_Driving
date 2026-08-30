# Handoff Notes

Read `README.md` first for the research framing (SST patent connection, why
the pipeline is shaped the way it is, and the V1-V4 iteration history). This
doc covers how to run things, what's actually done, and what's next - keep
it updated as the project moves forward.

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

(`mistral:instruct` does reasoning/decision, `qwen2.5vl:7b` does scene
description from images. Both are configured in `src/config.py` - swap either
for a different model or provider, see Next Steps below.)

Run everything from the repo root (scripts use relative paths like
`data/...`, `prompts/...`):

```bash
# full video -> frames -> vision -> reasoning -> decision pipeline
PYTHONPATH=src python3 src/run_pipeline.py data/raw/sample_construction_drive.mp4

# reasoning/decision against hand-authored scene JSON, or a folder of images
PYTHONPATH=src python3 src/run_scenario.py
```

`run_pipeline.py` prints Observation / Safety Self-Talk / Action / Explanation
per frame and logs full detail (scene.json, reasoning.txt, action.json,
summary.json) under `logs/pipeline_video_test/<video_name>/`.

---

## What's already implemented

- **`extract_frames.py`** - samples ~10 evenly-spaced frames from a video
  with opencv.
- **`vision_to_text.py`** - calls `qwen2.5vl:7b` via Ollama with
  `prompts/vision_scene_prompt.txt`, returns the structured scene JSON schema
  from `data/README.md` plus an `observation` field for a plain-language
  summary.
- **`sst_reasoning.py`** - takes an optional `history` list of prior frames'
  reasoning, so it can build evidence across frames instead of re-deriving it
  each time. Passing no history keeps single-frame behavior unchanged.
- **`run_pipeline.py`** - orchestrates video -> frames -> vision -> reasoning
  (with rolling history) -> decision, one frame at a time.
- **`run_scenario.py`** - runs reasoning + decision against hand-authored scene JSON in
  `data/test_scenes/` (no vision call - what produced the V1-V4 results), and
  has also been extended to run vision + reasoning + decision directly
  against a folder of images (see `logs/05_vision_crash_test/`).
- **`data/raw/sample_construction_drive.mp4`** - a synthetic test clip
  stitched from 5 stock images in `data/frames/construction_test/`, not a
  real dashcam clip. Used to confirm `run_pipeline.py` works end to end - see
  "Test video sourcing" for a real replacement. The logged run
  (`logs/pipeline_video_test/sample_construction_drive/`) shows the intended
  escalation pattern: `maintain_speed` through low-severity construction
  frames, `slow_down` once a stopped vehicle blocks the lane.

---

## Known issue: vision model doesn't infer risk

The v5 crash test (`logs/05_vision_crash_test/analysis.md`) found that
`qwen2.5vl:7b` correctly identifies objects (vehicles, debris, stopped cars)
but does **not** reliably infer hazard severity or path blockage - a clear
collision scene came back as `hazard_severity: medium` /
`path_status: clear or partially_blocked` when it should have been
`critical` / `blocked`. That under-reporting is what causes STOP to be
delayed or skipped downstream. This is the single most important known gap
right now (see Next Steps #1)

---

## Test video sourcing

Only the synthetic clip above and still images under `data/frames/` exist
right now. Places to get a real short clip, roughly best-fit first:

- **[Pexels](https://www.pexels.com/search/videos/dashcam/) /
  [Pixabay](https://pixabay.com/videos/search/dashcam/)** - free stock video,
  no-attribution license, short dashcam clips, direct download. Fastest path
  to something real.
- **[comma.ai open datasets](https://github.com/commaai)** (e.g. comma2k19) -
  real dashcam data released for research use, larger files.
- **[BDD100K](https://www.bdd100k.com/)** / **[KITTI](https://www.cvlibs.net/datasets/kitti/)**
  - already named in `data/README.md` for later-stage work. Larger,
    annotated, needs a free account for some splits - the right choice once
    you want ground-truth comparison, not just a smoke test.

Whatever you use, log the source/license/access date per `data/README.md`.

---

## Next Steps (priority order)

1. **Fix the vision model's risk-interpretation gap** (see above). Ideas
   from the v5 analysis: tighten `prompts/vision_scene_prompt.txt` to force
   explicit hazard/path reasoning, or add a rule-based mapping layer between
   raw vision output and the decision-facing scene JSON.
2. **Test against more real video**, across scenario types (construction,
   crash, pedestrian). Only one synthetic clip and one folder of crash
   stills have been run so far.
3. **Try alternative vision approaches** now that `qwen2.5vl:7b` is a known
   baseline, an API-hosted vision model (GPT-4V/Claude-vision-class) for a
   quality/cost comparison, YOLO for bounding-box object detection, or other
   small local VLMs.
4. **Try alternative LLM for reasoning** the current LLM for the sst reasoning 
    is `mistral:instruct`. Like #3, using an API-based LLM model (ChatGPT, Claude, etc.)
    may output stronger reasoning results than mistral: instruct. Additionally, finetuning 
    could be utilized.
5. **Decision layer tuning** (carried over from V1-V4): stronger STOP
   enforcement, better hazard_severity -> action mapping, less
   `maintain_speed` under real hazards.
6. **Evaluation framework** - compare system actions against human-labeled
   "correct" actions, not just eyeballing logs.
7. **Confidence calibration** - multi-run agreement / uncertainty estimation.
8. **Small cleanup items**:
   - No retry when the vision or decision model returns invalid JSON -
     currently just raises.
   - `decision_extraction.py` doesn't check the model's `action` is actually
     one of `ACTIONS`.
   - History passed to `sst_reason()` is raw text, unsummarized - fine now,
     would need trimming for longer sequences.
   - `test_file_name.py` is a global-variable hack for picking test
     filenames - should be a CLI arg.
   - `communication_modes.py` (audience-specific explanations) was planned
     but never built - low priority, Action + Explanation already cover it.
9. **Writeup** - most of the formal writeup still needs to happen. Test
   cases from `SST_AprilUpdatePowerpoint.pdf` (repo root) and the V1-V5
   analyses in `logs/*/analysis.md` are the raw material.

---

## Where to look

- `README.md` - research framing, setup/run instructions, V1-V4 history
- `logs/0N_full_test/analysis.md` - reasoning+decision only, pre-vision
- `logs/05_vision_crash_test/analysis.md` - the vision risk-interpretation finding
- `logs/pipeline_video_test/` - the video-based end-to-end run
- `src/README.md` - script-by-script description
- `data/README.md` - scene JSON schema and data sourcing notes
