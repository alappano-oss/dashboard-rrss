import pandas as pd
def top_posts(df,metric,n=10,ascending=False):
    if df.empty or metric not in df:return pd.DataFrame()
    cols=[c for c in ['date','platform','format','copy','reach','interactions','video_views','shares','comments','saves','url'] if c in df]
    return df.sort_values(metric,ascending=ascending,na_position='last')[cols].head(n).reset_index(drop=True)
