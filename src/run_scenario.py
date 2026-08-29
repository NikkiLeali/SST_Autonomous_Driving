# run_scenario.py

import json
from pathlib import Path
from sst_reasoning import sst_reason
from decision_extraction import extract_action
from vision_to_text import describe_image   # ← Make sure this import works

# NOTE: moved crash_images to data/raw/ to test smaller subset
BASE_IMAGE_DIR = Path("data/raw")   # Folder containing subfolders with images
BASE_LOG_DIR = Path("logs/05_vision_crash_test")

def run_all_scenarios():
    print("Starting vision-based scenario run...")

    # Get all subfolders (e.g. crash_sequence_1, crash_sequence_2, etc.)
    scenario_dirs = [d for d in BASE_IMAGE_DIR.iterdir() if d.is_dir()]

    if not scenario_dirs:
        print(f"No subfolders found in {BASE_IMAGE_DIR}")
        print("Make sure your images are inside subfolders like:")
        print("   data/frames/crash_images/crash_sequence_1/*.png")
        return

    for scenario_dir in scenario_dirs:
        scenario_name = scenario_dir.name
        print(f"\n====== Running scenario: {scenario_name} ======")

        # Get all image files
        image_files = sorted(scenario_dir.glob("*.png")) + \
                      sorted(scenario_dir.glob("*.jpg")) + \
                      sorted(scenario_dir.glob("*.jpeg"))

        if not image_files:
            print(f"   No image files found in {scenario_dir}")
            continue

        scenario_log_dir = BASE_LOG_DIR / scenario_name
        scenario_log_dir.mkdir(parents=True, exist_ok=True)

        summary = []

        for image_file in image_files:
            frame_id = image_file.stem   # e.g. "frame_001" or "img0001"

            print(f"--- Processing {frame_id} ({image_file.name}) ---")

            # === Step 1: Vision model → structured scene ===
            scene = describe_image(image_file)

            # === Step 2: SST Reasoning ===
            reasoning = sst_reason(scene)

            # === Step 3: Decision Extraction ===
            action = extract_action(scene, reasoning)

            # Save outputs
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

        # Save summary for this scenario
        summary_path = scenario_log_dir / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2))

        print(f"✅ Saved summary → {summary_path}")

    print("\nAll scenarios completed!")


if __name__ == "__main__":
    run_all_scenarios()
