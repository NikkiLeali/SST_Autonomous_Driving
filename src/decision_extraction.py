import json
import requests
from pathlib import Path
from test_file_name import test_name
from config import OLLAMA_URL, MODEL_NAME


# temporary list to be expanded
ACTIONS = [
    "maintain_speed",
    "slow_down",
    "stop",
    "merge_left",
    "merge_right",
    "yield"
]


def build_action_prompt(scene: dict, reasoning: str) -> str:
    return f"""
You are an autonomous driving decision module.

Scene description:
{json.dumps(scene, indent=2)}

Reasoning about the scene:
{reasoning}

Choose exactly ONE action from the following list:
{ACTIONS}

CRITICAL SAFETY RULES:
- If hazard_severity is "critical" AND hazard_proximity is "immediate", you MUST choose "stop"
- If path_status is "blocked", you MUST choose "stop"
- If hazard_severity is "high" and hazard_proximity is "near", prefer "stop" or "slow_down"
- If action_urgency is "immediate", prefer "stop"
- Only use "maintain_speed" if path_status is "clear" AND hazard_severity is "low"
- Use "yield" when interacting with other vehicles or pedestrians in shared space
- Use "merge_left" or "merge_right" when lane changes are required due to road conditions

You MUST follow these rules strictly.

Then provide:
- confidence (low, medium, or high)
- intent (why this action is chosen)
- fallback (what to do if the action cannot be safely executed)

Respond ONLY in valid JSON with this structure:

{{
  "action": "<one action from list>",
  "confidence": "<low|medium|high>",
  "intent": "<short explanation>",
  "fallback": "<backup action>"
}}
"""


def call_ollama(prompt: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    raw = response.json()["response"]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON:\n" + raw)


def extract_action(scene: dict, reasoning: str) -> dict:
    prompt = build_action_prompt(scene, reasoning)
    return call_ollama(prompt)


if __name__ == "__main__":
    # Load scene
    scene_path = Path(f"logs/{test_name}_scene.json")
    reasoning_path = Path(f"logs/{test_name}_reasoning.txt")
    output_path = Path(f"logs/{test_name}_action.json")

    assert scene_path.exists(), f"Missing scene file: {scene_path}"
    assert reasoning_path.exists(), f"Missing reasoning file: {reasoning_path}"

    with open(scene_path) as f:
        scene = json.load(f)

    reasoning = reasoning_path.read_text()

    action = extract_action(scene, reasoning)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(action, f, indent=2)
    
