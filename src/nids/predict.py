from pathlib import Path
import joblib, pandas as pd
from .preprocessing import clean_column_names
from .risk_scoring import risk_category

def load_artifacts(model_dir="models"):
    p=Path(model_dir)
    names=["imputer","scaler","isolation_forest","metadata"]
    missing=[n for n in names if not (p/f"{n}.joblib").exists()]
    if missing: raise FileNotFoundError("Missing trained artifacts: "+", ".join(missing)+". Run training after installing CIC-IDS2017.")
    return {n:joblib.load(p/f"{n}.joblib") for n in names}

def predict_frame(frame, a):
    df=clean_column_names(frame); info=a["metadata"]
    absent=[c for c in info["features"] if c not in df]
    if absent: raise ValueError("Missing required feature columns: "+", ".join(absent[:12]))
    X=df[info["features"]].apply(pd.to_numeric,errors="coerce").replace([float("inf"),float("-inf")],float("nan"))
    Xt=a["scaler"].transform(a["imputer"].transform(X))
    scores=-a["isolation_forest"].score_samples(Xt)
    risks=[risk_category(float(s),info["risk_cutoffs"]) for s in scores]
    out=df.copy(); out["anomaly_score"]=scores; out["is_anomaly"]=scores>=info["selected_threshold"]
    out["risk_category"]=[r[0] for r in risks]; out["recommended_action"]=[r[1] for r in risks]
    return out
