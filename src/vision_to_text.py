from PIL import Image
import json
from pathlib import Path
from test_file_name import test_name

def describe_image(image_path: Path) -> dict:
    # placeholder for vision-language model
    return {
        "scene": "highway driving",
        "objects": ["cars"],
        "conditions": "light traffic",
        "hazards": []
    }

if __name__ == "__main__":
    # TETS IMAGE PATH 
    image_path = Path("data/frames/test/istockphoto-1361912866-612x612.jpg")
    output_path = Path(f"logs/{test_name}.json")

    description = describe_image(image_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(description, f, indent=2)
