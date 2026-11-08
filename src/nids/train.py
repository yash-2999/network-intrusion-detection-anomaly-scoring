from pathlib import Path
import json, joblib
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from .config import load_config, ensure_dirs
from .data_loader import load_csv_files
from .preprocessing import clean_frame, fit_preprocessor, transform
from .models import PCAReconstructionDetector
from .threshold import thresholds_at_fpr

def main():
    cfg = load_config(); ensure_dirs(cfg)
    raw, manifest = load_csv_files(cfg["paths"]["raw_data"], cfg["data"]["chunksize"])
    X, y, meta, clean_report = clean_frame(raw)
    day = meta["__source_day"]
    benign = y.str.upper().eq("BENIGN")
    train_mask = day.isin(cfg["split"]["train_days"]) & benign
    val_mask = day.isin(cfg["split"]["validation_days"])
    if not train_mask.any() or not val_mask.any():
        raise ValueError("Need Monday BENIGN training rows and Tuesday validation rows.")
    imputer, scaler = fit_preprocessor(X.loc[train_mask])
    Xt = transform(X.loc[train_mask], imputer, scaler)
    Xv = transform(X.loc[val_mask], imputer, scaler)
    iso = IsolationForest(n_estimators=cfg["models"]["isolation_forest"]["n_estimators"],
                          random_state=cfg["random_seed"], n_jobs=-1).fit(Xt)
    pca = PCAReconstructionDetector(cfg["models"]["pca"]["variance_retained"]).fit(Xt)
    rfmask = day.isin(cfg["split"]["train_days"] + cfg["split"]["validation_days"])
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced_subsample",
                                random_state=cfg["random_seed"], n_jobs=-1)
    rf.fit(transform(X.loc[rfmask], imputer, scaler), (~benign.loc[rfmask]).astype(int))
    scores = -iso.score_samples(Xv)
    val_benign = benign.loc[val_mask].to_numpy()
    thresholds = thresholds_at_fpr(scores[val_benign], cfg["threshold"]["target_fpr"])
    selected_rate = min(thresholds, key=lambda r: abs(r-0.01))
    selected = thresholds[selected_rate]
    pca_scores = pca.score_samples(Xv)
    pca_thresholds = thresholds_at_fpr(pca_scores[val_benign], cfg["threshold"]["target_fpr"])
    pca_selected = pca_thresholds[selected_rate]
    b_scores = scores[val_benign]
    risk = {"medium": float(np.quantile(b_scores, cfg["risk"]["medium_quantile"])),
            "high": float(np.quantile(b_scores, cfg["risk"]["high_quantile"])),
            "critical": float(np.quantile(b_scores, cfg["risk"]["critical_quantile"]))}
    md = Path(cfg["paths"]["models"]); md.mkdir(exist_ok=True, parents=True)
    for name, obj in {"imputer":imputer, "scaler":scaler, "isolation_forest":iso,
                      "pca_reconstruction":pca, "random_forest":rf}.items():
        joblib.dump(obj, md/f"{name}.joblib")
    joblib.dump({"features":list(X.columns), "thresholds":thresholds,
                 "selected_threshold":selected, "pca_threshold":pca_selected, "pca_thresholds":pca_thresholds, "risk_cutoffs":risk,
                 "manifest":manifest.to_dict("records")}, md/"metadata.joblib")
    report = {"status":"trained", "rows":len(raw), "cleaning":clean_report,
              "train_benign_rows":int(train_mask.sum()), "validation_rows":int(val_mask.sum()),
              "thresholds":{str(k):v for k,v in thresholds.items()},
              "selected_threshold":selected, "pca_threshold":pca_selected, "selected_fpr_target":selected_rate, "supervised_rf_training_days":cfg["split"]["train_days"]+cfg["split"]["validation_days"]}
    Path(cfg["paths"]["reports"], "training_summary.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__": main()
