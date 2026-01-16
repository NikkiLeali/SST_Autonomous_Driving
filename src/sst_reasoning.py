import json
from pathlib import Path

def sst_reason(scene: dict) -> str:
    return (
        "The vehicle observes traffic ahead. "
        "There may be potential hazards. "
        "The safest action is to proceed cautiously."
    )

if __name__ == "__main__":
    scene_path = Path("logs/frame_001_scene.json")
    output_path = Path("logs/frame_001_reasoning.txt")

    with open(scene_path) as f:
        scene = json.load(f)

    reasoning = sst_reason(scene)

    with open(output_path, "w") as f:
        f.write(reasoning)
