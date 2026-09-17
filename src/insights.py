from __future__ import annotations
import pandas as pd


def generate_insights(df: pd.DataFrame, previous: pd.DataFrame | None = None) -> list[str]:
    insights=[]
    if df.empty: return insights
    if {'format','reach'}.issubset(df.columns):
        s=df.groupby('format')['reach'].mean().dropna().sort_values(ascending=False)
        if len(s)>=2:
            insights.append(f'{s.index[0]} registró mayor alcance promedio que {s.index[1]} durante el período analizado ({s.iloc[0]:,.0f} vs. {s.iloc[1]:,.0f}).')
    if {'format','shares'}.issubset(df.columns):
        share=df.groupby('format')['shares'].sum(min_count=1).dropna().sort_values(ascending=False)
        if len(share) and share.iloc[0] > 0:
            insights.append(f'El formato {share.index[0]} concentró la mayor cantidad de compartidos del período ({share.iloc[0]:,.0f}).')
    if {'date','reach'}.issubset(df.columns):
        x=df.copy(); x['date']=pd.to_datetime(x['date']); weekly=x.groupby(x['date'].dt.to_period('W'))['reach'].sum().dropna()
        if len(weekly)>=2:
            peak=weekly.idxmax(); insights.append(f"El mayor alcance acumulado se registró durante la semana iniciada el {peak.start_time.date().strftime('%d/%m/%Y')}.")
    if previous is not None and not previous.empty:
        from src.metrics import kpis
        a,b=kpis(df),kpis(previous)
        for label,key in [('alcance','reach_total'),('engagement','er_reach')]:
            av,bv=a.get(key),b.get(key)
            if pd.notna(av) and pd.notna(bv) and bv != 0:
                change=(av-bv)/abs(bv)*100
                insights.append(f'El {label} {"aumentó" if change>=0 else "disminuyó"} {abs(change):.1f}% respecto del período anterior.')
    return insights[:6]
