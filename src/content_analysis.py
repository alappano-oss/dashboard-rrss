from __future__ import annotations
import pandas as pd
from src.metrics import relative_performance


def top_contents(df: pd.DataFrame, metric: str, n=10) -> pd.DataFrame:
    if metric not in df: return pd.DataFrame()
    cols = [c for c in ['date','platform','format','copy','reach','interactions','er_reach','video_views','shares','comments','url'] if c in df]
    return df.dropna(subset=[metric]).sort_values(metric, ascending=False)[cols].head(n)


def format_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame()
    g = df.groupby('format', dropna=False)
    out = g.agg(cantidad=('format','size'), alcance_promedio=('reach','mean'), interacciones_promedio=('interactions','mean'), engagement_promedio=('er_reach','mean')).reset_index()
    return out.sort_values('alcance_promedio', ascending=False, na_position='last')


def weekday_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame()
    x = df.copy(); x['weekday'] = pd.to_datetime(x['date']).dt.day_name()
    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    g=x.groupby('weekday', observed=False).agg(publicaciones=('weekday','size'), alcance_promedio=('reach','mean'), engagement_promedio=('er_reach','mean')).reindex(order).reset_index()
    return g


def add_relative_performance(df: pd.DataFrame, metric='reach') -> pd.DataFrame:
    out=df.copy(); out['performance_relative']=relative_performance(out,metric); return out
