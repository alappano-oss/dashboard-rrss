import pandas as pd
def period_comparison(df,start,end):
    if df.empty:return pd.DataFrame()
    s=pd.Timestamp(start);e=pd.Timestamp(end);days=(e-s).days+1;d=pd.to_datetime(df.date,errors='coerce')
    cur=df[(d>=s)&(d<=e)];pe=s-pd.Timedelta(days=1);ps=pe-pd.Timedelta(days=days-1);prev=df[(d>=ps)&(d<=pe)];rows=[]
    for m in ['reach','interactions','video_views']:
        a=cur[m].sum(min_count=1);b=prev[m].sum(min_count=1);delta=a-b if pd.notna(a) and pd.notna(b) else pd.NA;pct=delta/b*100 if pd.notna(delta) and b!=0 else pd.NA;rows.append({'Métrica':m,'Actual':a,'Anterior':b,'Variación':delta,'%':pct})
    return pd.DataFrame(rows)
