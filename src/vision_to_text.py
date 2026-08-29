import base64
import json
from pathlib import Path

import requests

from config import OLLAMA_URL, VISION_MODEL_NAME

VISION_PROMPT_PATH = Path("prompts/vision_scene_prompt.txt")


def load_vision_prompt() -> str:
    assert VISION_PROMPT_PATH.exists(), f"Missing prompt file: {VISION_PROMPT_PATH}"
    return VISION_PROMPT_PATH.read_text()


def encode_image(image_path: Path) -> str:
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")


def call_ollama_vision(prompt: str, image_b64: str) -> str:
    payload = {
        "model": VISION_MODEL_NAME,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]


def describe_image(image_path: Path) -> dict:
    prompt = load_vision_prompt()
    image_b64 = encode_image(image_path)
    raw = call_ollama_vision(prompt, image_b64)

    try:
        scene = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("Vision model did not return valid JSON:\n" + raw)

    scene["frame_id"] = image_path.stem
    return scene


if __name__ == "__main__":
    # TEST IMAGE PATH
    image_path = Path("data/frames/test/istockphoto-1361912866-612x612.jpg")
    output_path = Path("logs/vision_test/test_scene.json")

    scene = describe_image(image_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(scene, f, indent=2)

    print(json.dumps(scene, indent=2))
