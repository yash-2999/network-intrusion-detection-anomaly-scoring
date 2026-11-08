import numpy as np
from src.nids.preprocessing import clean_frame
def test_clean_and_exclude(sample):
    X,y,meta,report=clean_frame(sample)
    assert "Source IP" not in X and "Destination Port" not in X and "Label" not in X
    assert len(X)==len(y)
def test_infinity(sample):
    sample.loc[0," Flow Duration "]=np.inf
    X,*_=clean_frame(sample)
    assert X["Flow Duration"].isna().sum()==1
