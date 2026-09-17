from __future__ import annotations
import numpy as np
import pandas as pd


def pct_change(current, previous):
    if pd.isna(current) or pd.isna(previous) or previous == 0: return np.nan
    return (current - previous) / abs(previous) * 100


def compare_kpis(current: dict, previous: dict) -> pd.DataFrame:
    rows=[]
    for key, value in current.items():
        prev = previous.get(key, np.nan)
        rows.append({'kpi':key,'current':value,'previous':prev,'absolute_change':value-prev if pd.notna(value) and pd.notna(prev) else np.nan,'percent_change':pct_change(value,prev)})
    return pd.DataFrame(rows)


def equivalent_previous_period(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.Timestamp,pd.Timestamp]:
    days = (end - start).days + 1
    prev_end = start - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=days-1)
    return prev_start, prev_end
