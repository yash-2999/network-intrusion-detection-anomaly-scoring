def explain_deviation(row, benign_reference, top_n=5):
    med = benign_reference.median()
    scale = benign_reference.std().replace(0, float("nan")).fillna(1.0)
    z = ((row[med.index] - med) / scale).replace([float("inf"), float("-inf")], 0).fillna(0)
    result = []
    for feature, value in z.abs().sort_values(ascending=False).head(top_n).items():
        result.append({"feature": feature, "direction": "above" if z[feature] >= 0 else "below",
                       "standardized_deviation": float(value)})
    return result
