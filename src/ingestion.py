from pathlib import Path
import pandas as pd
from src.data_loader import read_csv,infer_platform,infer_brand
from src.data_validator import validate_raw
from src.data_cleaner import normalize_dataframe,deduplicate
def ingest_files(files,brand):
    result={'files_processed':0,'new_records':0,'duplicates':0,'rejected':0,'errors':[],'warnings':[]};frames=[]
    for f in files:
        name=getattr(f,'name',None) or Path(str(f)).name
        try:
            raw=read_csv(f);v=validate_raw(raw);result['warnings'] += [f'{name}: {w}' for w in v.warnings]
            if not v.valid:
                result['rejected']+=1;result['errors'] += [f'{name}: {e}' for e in v.errors];continue
            detected=infer_brand(name,raw)
            if detected and detected!=brand:result['warnings'].append(f'{name}: se detectó {detected}; se procesará bajo {brand}.')
            frames.append(normalize_dataframe(raw,name,brand,infer_platform(name)));result['files_processed']+=1
        except Exception as e:result['rejected']+=1;result['errors'].append(f'{name}: {e}')
    if not frames:return pd.DataFrame(),result
    combined,dups=deduplicate(None,pd.concat(frames,ignore_index=True));result['duplicates']=dups;result['new_records']=len(combined);return combined,result
