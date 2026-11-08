import numpy as np

def thresholds_at_fpr(benign_scores, targets=(0.01, 0.05)):
    scores = np.asarray(benign_scores, dtype=float)
    scores = scores[np.isfinite(scores)]
    if not len(scores):
        raise ValueError("No finite benign validation scores.")
    return {float(r): float(np.quantile(scores, 1-r, method="higher")) for r in targets}
