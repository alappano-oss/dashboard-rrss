import pandas as pd
def kpis(df):
    if df.empty:return {}
    def total(c):return float(df[c].sum(min_count=1)) if c in df else None
    def mean(c):return float(df[c].mean()) if c in df else None
    return {'Publicaciones':len(df),'Alcance total':total('reach'),'Alcance promedio':mean('reach'),'Interacciones':total('interactions'),'ER promedio por alcance':float(df.er_reach.mean()) if 'er_reach' in df else None,'Visualizaciones':total('video_views')}
def by_format(df):
    if df.empty:return pd.DataFrame()
    return df.groupby('format',dropna=False).agg(publicaciones=('post_id','count'),alcance=('reach','sum'),interacciones=('interactions','sum'),visualizaciones=('video_views','sum')).reset_index()
