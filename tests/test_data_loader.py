import pytest
from src.nids.data_loader import infer_day
def test_day(): assert infer_day("Monday-WorkingHours.csv")=="Monday"
def test_unknown_day():
    with pytest.raises(ValueError): infer_day("unknown.csv")
