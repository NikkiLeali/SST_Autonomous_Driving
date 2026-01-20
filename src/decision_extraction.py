import json
from pathlib import Path
from test_file_name import test_name 

def extract_action(reasoning: str) -> dict:
    return {
        "action": "slow_down",
        "confidence": 0.5,
        "justification": "uncertain environment"
    }

if __name__ == "__main__":
    reasoning_path = Path(f"logs/{test_name}_reasoning.txt")
    output_path = Path(f"logs/{test_name}_action.json")

    reasoning = reasoning_path.read_text()
    action = extract_action(reasoning)

    with open(output_path, "w") as f:
        json.dump(action, f, indent=2)
