from pathlib import Path
import hashlib
import pandas as pd

def infer_day(filename):
    name = Path(filename).name.lower()
    for day in ("monday", "tuesday", "wednesday", "thursday", "friday"):
        if day in name:
            return day.title()
    raise ValueError(f"Cannot infer collection day from filename: {filename}")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_csv_files(raw_dir, chunksize=100000):
    paths = sorted(Path(raw_dir).glob("*.csv"))
    if not paths:
        raise FileNotFoundError(f"No CIC-IDS2017 CSVs in {raw_dir}. Download the genuine dataset from https://www.unb.ca/cic/datasets/ids-2017.html")
    frames, manifest = [], []
    for path in paths:
        day = infer_day(path.name)
        count = 0
        for chunk in pd.read_csv(path, chunksize=chunksize, low_memory=False):
            chunk["__source_day"] = day
            count += len(chunk)
            frames.append(chunk)
        manifest.append({"filename": path.name, "day": day, "rows": count, "sha256": sha256_file(path)})
    return pd.concat(frames, ignore_index=True), pd.DataFrame(manifest)

if __name__ == "__main__":
    from .config import load_config
    cfg = load_config()
    df, manifest = load_csv_files(cfg["paths"]["raw_data"], cfg["data"]["chunksize"])
    print(f"Loaded {len(df):,} rows from {len(manifest)} files")
    print(manifest.to_string(index=False))
