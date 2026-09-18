import hashlib,numpy as np,pandas as pd
from config.config import CANONICAL_COLUMNS,FORMAT_MAP,NUMERIC_COLUMNS,PLATFORM_MAP
from src.data_validator import resolve_columns
from src.data_loader import infer_platform
def normalize_format(v):
    if pd.isna(v):return pd.NA
    r=str(v).strip().lower()
    if r in FORMAT_MAP:return FORMAT_MAP[r]
    if 'reel' in r:return 'Reel'
    if 'secuencia' in r or 'carrusel' in r or 'carousel' in r:return 'Carrusel'
    if 'video' in r or 'vídeo' in r:return 'Video'
    if 'foto' in r or 'imagen' in r:return 'Imagen'
    return str(v).strip()
def num(v):
    if pd.isna(v) or str(v).strip()=='':return np.nan
    s=str(v).strip().replace(' ','')
    try:return float(s.replace(',','.'))
    except ValueError:
        try:return float(s.replace('.','').replace(',','.'))
        except ValueError:return np.nan
def key(r):
    base=[r.get('brand',''),r.get('platform',''),r.get('post_id','')]
    if not str(r.get('post_id','')).strip() or str(r.get('post_id',''))=='<NA>':base += [r.get('account',''),r.get('date',''),r.get('url',''),r.get('copy','')]
    return hashlib.sha1('|'.join(map(str,base)).encode()).hexdigest()
def normalize_dataframe(raw,filename,brand,platform=None):
    m=resolve_columns(raw.columns);out=pd.DataFrame(index=raw.index)
    for c in CANONICAL_COLUMNS:out[c]=pd.NA
    out['brand']=brand;out['platform']=platform or infer_platform(filename) or pd.NA;out['source_file']=filename;out['source_row']=np.arange(1,len(raw)+1)
    for c,s in m.items():out[c]=raw[s]
    if 'published_datetime' in m:
        dt=pd.to_datetime(raw[m['published_datetime']],errors='coerce',format='mixed',dayfirst=False)
        out['published_datetime']=dt;out['date']=dt.dt.date;out['time']=dt.dt.strftime('%H:%M:%S')
    if 'format' in m:out['format']=out['format'].map(normalize_format)
    out['platform']=out['platform'].map(lambda x:PLATFORM_MAP.get(str(x).lower(),x) if pd.notna(x) else x)
    for c in NUMERIC_COLUMNS:out[c]=out[c].map(num).astype('Float64')
    derived=pd.concat([out[c] for c in ('likes','comments','shares','saves')],axis=1).sum(axis=1,min_count=1)
    out['interactions']=out['interactions'].where(out['interactions'].notna(),derived)
    out['er_reach']=np.where(out['reach'].notna()&(out['reach']!=0)&out['interactions'].notna(),out['interactions']/out['reach']*100,np.nan)
    out['er_impressions']=np.where(out['impressions'].notna()&(out['impressions']!=0)&out['interactions'].notna(),out['interactions']/out['impressions']*100,np.nan)
    out['_record_key']=out.apply(key,axis=1);return out
def deduplicate(existing,incoming):
    combined=incoming.copy() if existing is None or existing.empty else pd.concat([existing,incoming],ignore_index=True);before=len(combined)
    return combined.drop_duplicates('_record_key',keep='first').reset_index(drop=True),before-len(combined)
