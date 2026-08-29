# Handoff Notes

Read `README.md` first for the research framing (SST patent connection, why
the pipeline is shaped the way it is, and the V1-V4 iteration history). This
doc is the practical "how do I run this, what's actually done, and what's
next" companion - it's the one to keep updated as the project moves forward.

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
scene description from images. Both are configured in `src/config.py` - swap
either for a different local model name, or a different provider entirely,
see "Next Steps" below.)

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

## What's actually implemented

- **`extract_frames.py`** - samples ~10 evenly-spaced frames from a video with
  opencv.
- **`vision_to_text.py`** - real vision-model call (was a hardcoded stub
  before this pass). Sends the frame to `qwen2.5vl:7b` via Ollama with
  `prompts/vision_scene_prompt.txt`, gets back the same structured scene JSON
  schema documented in `data/README.md` (plus a new `observation` field for a
  plain-language summary).
- **`sst_reasoning.py`** - takes an optional `history` list (prior frames'
  reasoning text). `run_pipeline.py` passes a rolling window
  (`HISTORY_WINDOW` in `config.py`, default 3) so reasoning can build evidence
  across frames instead of re-deriving it each time - this is the "brake
  lights -> cones -> blocked lane" behavior described for the project.
  `run_scenario.py` doesn't pass history (single-frame scenes), so it's
  unaffected.
- **`run_pipeline.py`** - orchestrator tying the above together. Doesn't
  replace `run_scenario.py`, which is still the right tool for iterating on
  reasoning/decision prompts without a vision call in the loop.
- **`data/raw/sample_construction_drive.mp4`** - a synthetic test clip
  stitched from `data/frames/construction_test/` (there was no raw video in
  the repo) so `run_pipeline.py` has something to run against. It's 5 source
  images held for a few frames each, not an actual dashcam clip - see "Test
  video sourcing" below for a real replacement. A run against it is logged at
  `logs/pipeline_video_test/sample_construction_drive/` and shows the
  escalation pattern working: `maintain_speed` through the early
  low-severity construction frames, then `slow_down` once a stopped vehicle
  blocks the lane.

---

## Test video sourcing

No real driving footage is in the repo yet - only the synthetic clip above
and the still images under `data/frames/`. Good places to get a real short
clip to test with, roughly in order of how usable the footage is for this
prototype:

- **[Pexels](https://www.pexels.com/search/videos/dashcam/) /
  [Pixabay](https://pixabay.com/videos/search/dashcam/)** - free stock video,
  clear licensing (no attribution required, safe to check in if you want),
  short dashcam/driving clips, easy to download directly. Fastest path to a
  real test clip.
- **[comma2k9 / comma.ai research datasets](https://github.com/commaai)** -
  real dashcam driving data released for research use, larger files.
- **[BDD100K](https://www.bdd100k.com/)** and
  **[KITTI](https://www.cvlibs.net/datasets/kitti/)** - the two datasets
  `data/README.md` already calls out for later-stage work. Larger downloads,
  annotated, require a (free) account/agreement for some splits - the right
  choice once you're past smoke-testing and want to evaluate against
  ground-truth labels.

Whatever you use, `data/README.md` already asks for source/license/access
date to be documented - worth doing right away so it doesn't get lost.

---

## Next Steps

Rough priority order, though the two "still needs full testing" items below
are probably the highest-value thing to spend time on before anything else,
since almost nothing past the smoke tests in this handoff has been run
against real footage.

**1. Full testing & refinement against real video** - everything vision-side
has only been run against one 5-frame synthetic clip. Needs real dashcam
footage (see above) across multiple scenario types (construction, crash,
pedestrian - mirroring the existing `data/test_scenes/` categories) before
any of the reasoning/decision behavior can be trusted.

**2. Try alternative vision models / providers** - `qwen2.5vl:7b` via Ollama
was the first thing that was already available locally, not a considered
choice. Worth comparing:
- An API-based vision model (e.g. hosted GPT-4V/Claude-vision-class model)
  instead of local Ollama, for a quality/latency/cost comparison.
- Object-detection-first approaches like YOLO for a bounding-box object list
  instead of (or feeding into) free-form VLM description.
- Other small local VLMs if inference speed matters.

**3. Decision layer tuning** (carried over from earlier iterations, still
true post-vision):
- Strengthen STOP enforcement rules
- Improve mapping: hazard_severity → action
- Reduce maintain_speed usage when hazards are present
- Improve early-stage hazard response (pre-escalation behavior)

**4. Evaluation framework** - compare system actions against human-labeled
"correct" actions per scenario; measure correctness and safety, not just
"does it run."

**5. Confidence calibration** - multi-run agreement / uncertainty estimation
across repeated runs of the same scene.

**6. Smaller fixes**, lower priority but cheap to do whenever someone's in
that file:
- No retry/re-prompt when `vision_to_text.py` or `decision_extraction.py`
  get back invalid JSON from the model - currently just raises.
- `decision_extraction.py` doesn't validate that the returned `action` is
  actually one of the values in `ACTIONS` - it trusts the model's compliance
  with the prompt instructions.
- History passed to `sst_reason()` is raw reasoning text, unsummarized -
  fine for ~10 frames, would need condensing for longer sequences.
- `test_file_name.py` is a fragile global-variable hack used by several
  scripts' `__main__` blocks to pick a test file name - should be a CLI arg
  or function parameter instead.
- `run_scenario.py` hardcodes its output dir to `logs/04_full_test` - each
  new iteration means manually bumping that path.
- `communication_modes.py` (audience-specific explanations) was in the
  original plan in `src/README.md` but was never built - low priority, the
  Action + Explanation fields already cover the core loop.

**7. Writeup** - most of the formal writeup still needs to happen. `docs/`
exists for this (method drafts, figures, experiment tables - see
`docs/README.md`) but is currently empty. The V1-V4 analysis in
`logs/0N_full_test/analysis.md` and the results table in `README.md` are the
existing raw material to draw from.

**8. April test-case slides** - referenced as showing test cases clearly, but
not present in this branch/worktree - add the file (`docs/` seems like the
right home) and it can be linked from here and cross-referenced against the
`logs/` results.

---

## Where to look

- `README.md` - research framing, setup/run instructions, and the V1-V4
  iteration history/results
- `logs/0N_full_test/analysis.md` - per-version writeups of what changed and
  what the model actually did (reasoning+decision only, pre-vision)
- `logs/pipeline_video_test/` - the video-based end-to-end run
- `src/README.md` - script-by-script description
- `data/README.md` - scene JSON schema and data sourcing notes
