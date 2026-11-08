import yaml
from pathlib import Path

def load_config(path="configs/config.yaml"):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dirs(cfg):
    for key in ("raw_data", "models", "reports"):
        Path(cfg["paths"][key]).mkdir(parents=True, exist_ok=True)
