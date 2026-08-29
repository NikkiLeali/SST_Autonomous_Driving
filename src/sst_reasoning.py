import json
import requests
from pathlib import Path
from test_file_name import test_name
from config import OLLAMA_URL, MODEL_NAME


PROMPT_PATH = Path("prompts/sst_reasoning_base_prompt.txt")

def load_prompt_template() -> str:
    assert PROMPT_PATH.exists(), f"Missing prompt file: {PROMPT_PATH}"
    return PROMPT_PATH.read_text()

def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]

def sst_reason(scene: dict, history: list[str] | None = None) -> str:
    template = load_prompt_template()
    scene_text = json.dumps(scene, indent=2)

    # history = prior frames' reasoning, oldest to most recent, so SST can build
    # on earlier uncertainty instead of re-reasoning each frame from scratch
    if history:
        history_text = "\n\n".join(
            f"Frame {i + 1} reasoning:\n{h}" for i, h in enumerate(history)
        )
        scene_text = (
            f"Prior frame observations (oldest to most recent):\n{history_text}\n\n"
            f"Current frame scene description:\n{scene_text}"
        )

    prompt = template.format(scene=scene_text)
    return call_ollama(prompt)

if __name__ == "__main__":
    scene_path = Path(f"logs/{test_name}.json")
    output_path = Path(f"logs/{test_name}_reasoning.txt")

    assert scene_path.exists(), f"Missing input file: {scene_path}"

    with open(scene_path) as f:
        scene = json.load(f)

    reasoning = sst_reason(scene)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(reasoning)
