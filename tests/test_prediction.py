import pandas as pd, pytest
from src.nids.predict import predict_frame
def test_missing_feature():
    a={"metadata":{"features":["Flow Duration"]}}
    with pytest.raises(ValueError): predict_frame(pd.DataFrame({"wrong":[1]}),a)
