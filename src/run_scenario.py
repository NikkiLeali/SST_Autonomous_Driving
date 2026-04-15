# run_scenario.py

import json
from pathlib import Path
from sst_reasoning import sst_reason
from decision_extraction import extract_action

BASE_SCENE_DIR = Path("data/test_scenes")
BASE_LOG_DIR = Path("logs/02_full_test")

def run_all_scenarios():
    scenario_dirs = [d for d in BASE_SCENE_DIR.iterdir() if d.is_dir()]

    for scenario_dir in scenario_dirs:
        scenario_name = scenario_dir.name
        print(f"\n====== Running scenario: {scenario_name} ======")

        files = sorted(scenario_dir.glob("*.json"))
        scenario_log_dir = BASE_LOG_DIR / scenario_name
        scenario_log_dir.mkdir(parents=True, exist_ok=True)

        summary = []

        for scene_file in files:
            with open(scene_file) as f:
                scene = json.load(f)

            frame_id = scene["frame_id"]

            print(f"--- Processing {frame_id} ---")

            reasoning = sst_reason(scene)
            action = extract_action(reasoning)

            # Save per-frame outputs
            out_dir = scenario_log_dir / frame_id
            out_dir.mkdir(parents=True, exist_ok=True)

            (out_dir / "scene.json").write_text(json.dumps(scene, indent=2))
            (out_dir / "reasoning.txt").write_text(reasoning)
            (out_dir / "action.json").write_text(json.dumps(action, indent=2))

            # Add to summary
            summary.append({
                "frame_id": frame_id,
                "scene_type": scene.get("scene_type", "unknown"),
                "action": action.get("action"),
                "confidence": action.get("confidence"),
                "intent": action.get("intent")
            })

        # Save summary file
        summary_path = scenario_log_dir / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2))

        print(f"Saved summary → {summary_path}")


if __name__ == "__main__":
    run_all_scenarios()
