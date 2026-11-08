import numpy as np
from src.nids.models import PCAReconstructionDetector
from src.nids.threshold import thresholds_at_fpr
def test_pca():
    X=np.random.default_rng(42).normal(size=(40,5))
    assert (PCAReconstructionDetector(.9).fit(X).score_samples(X)>=0).all()
def test_threshold():
    t=thresholds_at_fpr(np.arange(100),(0.05,))
    assert t[0.05]>=94
