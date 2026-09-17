from __future__ import annotations
import pandas as pd
import plotly.express as px


def time_series(df, metric, freq='W'):
    if df.empty or metric not in df: return None
    x=df.copy(); x['date']=pd.to_datetime(x['date']); x=x.dropna(subset=['date',metric])
    if x.empty: return None
    agg=x.set_index('date').resample(freq)[metric].sum().reset_index()
    return px.line(agg, x='date', y=metric, markers=True, title=metric.replace('_',' ').title())


def bar_summary(df, x, y, title=None):
    if df.empty or x not in df or y not in df: return None
    return px.bar(df, x=x, y=y, title=title)


def horizontal_ranking(df, metric, title):
    if df.empty or metric not in df: return None
    x=df.copy().dropna(subset=[metric]).sort_values(metric).head(10)
    x['label']=x.get('copy', pd.Series('',index=x.index)).astype(str).str.slice(0,60)
    return px.bar(x, x=metric, y='label', orientation='h', title=title)
