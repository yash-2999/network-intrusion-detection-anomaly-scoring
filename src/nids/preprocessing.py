import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

DROP = {"flow id", "source ip", "destination ip", "source port",
        "timestamp", "destination port", "__source_day"}

def clean_column_names(df):
    out = df.copy()
    seen, names = {}, []
    for raw in out.columns:
        name = str(raw).strip()
        n = seen.get(name, 0)
        seen[name] = n + 1
        names.append(name if n == 0 else f"{name}__dup{n}")
    out.columns = names
    return out

def clean_frame(df):
    out = clean_column_names(df).drop_duplicates().reset_index(drop=True).copy()
    label_cols = [c for c in out.columns if c.lower() == "label"]
    if not label_cols:
        raise ValueError("Required Label column is missing.")
    y = out[label_cols[0]].astype(str).str.strip().reset_index(drop=True)
    feature_cols = [c for c in out.columns if c != label_cols[0] and c.lower() not in DROP]
    X = out[feature_cols].apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan).dropna(axis=1, how="all")
    metadata = out.reset_index(drop=True)
    return X.astype("float32"), y, metadata, {"rows": len(out), "features": list(X.columns)}

def fit_preprocessor(X):
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    values = imputer.fit_transform(X)
    scaler.fit(values)
    return imputer, scaler

def transform(X, imputer, scaler):
    return scaler.transform(imputer.transform(X)).astype("float32")
