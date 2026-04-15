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

# future: confidence can be numeric 0-1 with multiple adversarial LLM runs, aggregating the result


def build_action_prompt(reasoning: str) -> str:
    return f"""
You are an autonomous driving decision module.

Based on the following reasoning:
{reasoning}

Choose exactly ONE action from the following list:
{ACTIONS}

IMPORTANT DECISION RULES:
- If there is an immediate hazard (collision, pedestrian in path, blocked lane), you MUST choose "stop"
- If the situation is evolving or uncertain, choose "slow_down"
- Only choose "maintain_speed" when the scene is clearly safe and stable
- Use "yield" when interacting with other vehicles or pedestrians in shared space based on right-of-way rules
- Use "merge_left" or "merge_right" when lane changes are required due to road conditions
- Ensure all decision actions prioritizes safety (both for the vehicle and surrounding entities) above all else.

Your decision must reflect the severity of the situation.

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

def extract_action(reasoning: str) -> dict:
    prompt = build_action_prompt(reasoning)
    return call_ollama(prompt)

if __name__ == "__main__":
    reasoning_path = Path(f"logs/{test_name}_reasoning.txt")
    output_path = Path(f"logs/{test_name}_action.json")

    assert reasoning_path.exists(), f"Missing reasoning file: {reasoning_path}"

    reasoning = reasoning_path.read_text()
    action = extract_action(reasoning)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(action, f, indent=2)
