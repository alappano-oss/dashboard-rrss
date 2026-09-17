import pandas as pd
from src.comparisons import pct_change,equivalent_previous_period

def test_pct_change(): assert round(pct_change(245,198),2)==23.74

def test_previous_period():
    s,e=pd.Timestamp('2026-08-01'),pd.Timestamp('2026-08-31')
    ps,pe=equivalent_previous_period(s,e)
    assert ps==pd.Timestamp('2026-07-01') and pe==pd.Timestamp('2026-07-31')
