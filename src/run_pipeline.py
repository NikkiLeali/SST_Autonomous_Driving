# run_pipeline.py
# Full video -> frames -> vision -> SST reasoning -> decision path.
# run_scenario.py stays separate - it's the hand-authored-scene test harness
# used for the versioned reasoning/decision experiments in logs/.

import json
import sys
from pathlib import Path

from extract_frames import extract_frames
from vision_to_text import describe_image
from sst_reasoning import sst_reason
from decision_extraction import extract_action
from config import NUM_FRAMES, HISTORY_WINDOW


def run_pipeline(video_path: Path, log_dir: Path, num_frames: int = NUM_FRAMES) -> None:
    frame_dir = Path("data/frames") / video_path.stem
    frame_paths = extract_frames(video_path, frame_dir, num_frames=num_frames)

    log_dir.mkdir(parents=True, exist_ok=True)
    history = []
    summary = []

    for frame_path in frame_paths:
        frame_id = frame_path.stem
        print(f"\n====== Frame: {frame_id} ======")

        scene = describe_image(frame_path)
        reasoning = sst_reason(scene, history=history[-HISTORY_WINDOW:])
        action = extract_action(scene, reasoning)

        history.append(reasoning)

        out_dir = log_dir / frame_id
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "scene.json").write_text(json.dumps(scene, indent=2))
        (out_dir / "reasoning.txt").write_text(reasoning)
        (out_dir / "action.json").write_text(json.dumps(action, indent=2))

        print(f"Observation: {scene.get('observation', '')}")
        print(f"Safety Self-Talk: {reasoning}")
        print(f"Action: {action.get('action')}")
        print(f"Explanation: {action.get('intent')}")

        summary.append({
            "frame_id": frame_id,
            "action": action.get("action"),
            "confidence": action.get("confidence"),
            "intent": action.get("intent"),
        })

    summary_path = log_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\nSaved summary -> {summary_path}")


if __name__ == "__main__":
    # TEST VIDEO PATH
    video_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/raw/sample_construction_drive.mp4")
    log_dir = Path("logs/pipeline_video_test") / video_path.stem

    run_pipeline(video_path, log_dir)
