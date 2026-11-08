from pathlib import Path
import json, joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
from .config import load_config
from .data_loader import load_csv_files
from .preprocessing import clean_frame, transform

def calculate_metrics(truth, scores, threshold):
    pred=(scores>=threshold).astype(int)
    tn,fp,fn,tp=confusion_matrix(truth,pred,labels=[0,1]).ravel()
    def auc(fn):
        try: return float(fn(truth,scores))
        except ValueError: return None
    return {"accuracy":float(accuracy_score(truth,pred)),
      "precision":float(precision_score(truth,pred,zero_division=0)),
      "recall":float(recall_score(truth,pred,zero_division=0)),
      "f1":float(f1_score(truth,pred,zero_division=0)),
      "roc_auc":auc(roc_auc_score),"pr_auc":auc(average_precision_score),
      "confusion_matrix":[[int(tn),int(fp)],[int(fn),int(tp)]],
      "false_positive_rate":float(fp/(fp+tn)) if fp+tn else None,
      "true_positive_rate":float(tp/(tp+fn)) if tp+fn else None,
      "positive_prevalence":float(truth.mean()),"random_pr_auc_baseline":float(truth.mean())}

def main():
    cfg=load_config()
    raw,_=load_csv_files(cfg["paths"]["raw_data"],cfg["data"]["chunksize"])
    X,y,meta,_=clean_frame(raw)
    mask=meta["__source_day"].isin(cfg["split"]["test_days"])
    md=Path(cfg["paths"]["models"])
    imp=joblib.load(md/"imputer.joblib"); scaler=joblib.load(md/"scaler.joblib")
    info=joblib.load(md/"metadata.joblib")
    Xt=transform(X.loc[mask],imp,scaler)
    truth=(~y.loc[mask].str.upper().eq("BENIGN")).astype(int).to_numpy()
    iso=joblib.load(md/"isolation_forest.joblib")
    pca=joblib.load(md/"pca_reconstruction.joblib")
    rf=joblib.load(md/"random_forest.joblib")
    results={
      "isolation_forest":calculate_metrics(truth,-iso.score_samples(Xt),info["selected_threshold"]),
      "pca_reconstruction":calculate_metrics(truth,pca.score_samples(Xt),info["pca_threshold"]),
      "random_forest":calculate_metrics(truth,rf.predict_proba(Xt)[:,1],0.5)
    }
    result={"models":results,"test_rows":int(mask.sum()),"thresholds_frozen_before_test":True,
            "note":"RF is supervised and trained on labeled Monday+Tuesday data; unsupervised detectors fit Monday BENIGN only."}
    rp=Path(cfg["paths"]["reports"]); rp.mkdir(exist_ok=True,parents=True)
    (rp/"metrics.json").write_text(json.dumps(result,indent=2))
    rows=[]
    for name,metrics in results.items(): rows.append({"model":name,**{k:v for k,v in metrics.items() if k!="confusion_matrix"}})
    pd.DataFrame(rows).to_csv(rp/"model_comparison.csv",index=False)
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
