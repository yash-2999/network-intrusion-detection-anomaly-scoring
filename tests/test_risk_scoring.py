from src.nids.risk_scoring import risk_category
def test_bands():
    c={"medium":2,"high":3,"critical":4}
    assert [risk_category(i,c)[0] for i in (1,2,3,4)]==["LOW","MEDIUM","HIGH","CRITICAL"]
