from pathlib import Path
import json

def load_state(path):
    if not path.exists(): return {}
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: raise ValueError(f"Invalid state file: {path}") from exc
    if not isinstance(data,dict): raise ValueError("State file must contain a JSON object")
    return {str(k):str(v) for k,v in data.items()}

def save_state(path, state):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(state,indent=2,ensure_ascii=False,sort_keys=True),encoding="utf-8")
