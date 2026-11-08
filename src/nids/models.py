import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.decomposition import PCA

class PCAReconstructionDetector:
    def __init__(self, variance_retained=0.95):
        self.variance_retained = variance_retained
    def fit(self, X):
        self.pca_ = PCA(n_components=self.variance_retained, svd_solver="full").fit(X)
        return self
    def score_samples(self, X):
        reconstructed = self.pca_.inverse_transform(self.pca_.transform(X))
        return np.mean((X - reconstructed) ** 2, axis=1)

def anomaly_scores(model, X, name):
    return -model.score_samples(X) if name == "isolation_forest" else model.score_samples(X)
