import pandas as pd, pytest
from src.nids.split import day_based_split
def test_disjoint():
    df=pd.DataFrame({"__source_day":["Monday","Tuesday","Wednesday"],"id":[1,2,3]})
    a,b,c=day_based_split(df,test_days=("Wednesday",))
    assert set(a.id).isdisjoint(set(b.id)) and set(b.id).isdisjoint(set(c.id))
def test_missing():
    with pytest.raises(ValueError): day_based_split(pd.DataFrame({"__source_day":["Monday"]}))
