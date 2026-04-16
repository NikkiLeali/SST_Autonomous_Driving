from PIL import Image
import json
import ollama
from pathlib import Path
from test_file_name import test_name

def describe_image(image_path: Path) -> dict:
    """
    Uses Qwen2.5-VL-7B to analyze a dashcam image and return structured scene description.
    """
    image_path = Path(image_path).resolve()

    prompt = """
You are an autonomous driving perception module for a Safety Self-Talk (SST) system.
Analyze the dashcam image and output **ONLY** valid JSON using this exact schema.
Do not add any explanation or extra text before or after the JSON.

{
  "scene_type": "construction_zone | crash | pedestrian | highway | intersection | normal | other",
  "frame_id": "",
  "road_type": "highway | urban | rural | construction | ...",
  "hazard_severity": "low | medium | high",
  "hazard_proximity": "far | medium | close | immediate",
  "path_status": "clear | partially_blocked | fully_blocked",
  "traffic_density": "low | medium | high",
  "visibility": "good | moderate | poor | night | glare",
  "key_objects": ["orange_barrels", "stopped_vehicle", "pedestrian", "debris", ...],
  "ego_vehicle_state": {
    "speed": "high | medium | low",
    "lane_position": "left | center | right | merging"
  },
  "brief_reasoning": "1-2 sentences of safety self-talk style assessment"
}

Be safety-focused and conservative with hazard_severity.
"""

    try:
        response = ollama.chat(
            model="qwen2.5vl:7b",
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [str(image_path)]
            }]
        )

        content = response['message']['content'].strip()

        # Extract JSON block (Qwen sometimes adds extra text)
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end > start:
            scene_data = json.loads(content[start:end])
            return scene_data
        else:
            raise ValueError("No JSON found")

    except Exception as e:
        print(f"Vision model error: {e}")
        # Safe fallback so your pipeline doesn't break
        return {
            "scene_type": "unknown",
            "hazard_severity": "medium",
            "path_status": "partially_blocked",
            "key_objects": [],
            "brief_reasoning": "Vision model failed. Using safe default."
        }


if __name__ == "__main__":
    # Test image path
    image_path = Path("data/frames/test/istockphoto-1361912866-612x612.jpg")
    output_path = Path(f"logs/{test_name}.json")

    print(f"Analyzing image: {image_path.name}")
    description = describe_image(image_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(description, f, indent=2)

    print(f"Saved scene description to: {output_path}")
    print(json.dumps(description, indent=2))