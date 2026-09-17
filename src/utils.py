from __future__ import annotations
import math
import pandas as pd


def fmt_number(value, decimals=0):
    if value is None or (isinstance(value,float) and math.isnan(value)): return '—'
    return f'{value:,.{decimals}f}'.replace(',', 'X').replace('.', ',').replace('X','.')


def fmt_pct(value, decimals=1):
    if value is None or pd.isna(value): return '—'
    sign='+' if value > 0 else ''
    return f'{sign}{value:.{decimals}f}%'.replace('.', ',')
