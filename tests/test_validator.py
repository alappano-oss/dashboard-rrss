import pandas as pd
from src.data_validator import validate_raw

def test_required_columns():
    r=validate_raw(pd.DataFrame({'date':['01/08/2026'],'platform':['Instagram']}))
    assert r.valid

def test_missing_columns():
    r=validate_raw(pd.DataFrame({'foo':[1]}))
    assert not r.valid and len(r.errors)>=2
