import numpy as np, pandas as pd, pytest
@pytest.fixture
def sample():
    rng=np.random.default_rng(42)
    return pd.DataFrame({" Flow Duration ":rng.normal(size=30)," Source IP":["10.0.0.1"]*30,
      "Destination Port":[443]*30," Label":["BENIGN"]*20+["DoS"]*10,
      "__source_day":["Monday"]*10+["Tuesday"]*10+["Wednesday"]*10})
