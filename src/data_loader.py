from pathlib import Path
from io import BytesIO
import pandas as pd
def read_csv(source):
    data=source.getvalue() if hasattr(source,'getvalue') else (bytes(source) if isinstance(source,(bytes,bytearray)) else Path(source).read_bytes())
    last=None
    for enc in ('utf-8-sig','utf-8','latin-1'):
        try:return pd.read_csv(BytesIO(data),encoding=enc)
        except Exception as e:last=e
    raise ValueError(f'No se pudo leer el CSV: {last}')
def infer_platform(filename):
    n=Path(str(filename)).name.upper()
    return 'Facebook' if n.startswith('FB-') else ('Instagram' if n.startswith('IG-') else None)
def infer_brand(filename,df=None):
    text=str(filename).lower()
    if df is not None:
        for c in ('Nombre de la página','Nombre de la cuenta','Nombre de usuario de la cuenta'):
            if c in df.columns:text+=' '+' '.join(df[c].dropna().astype(str).head(10)).lower()
    if 'elebar' in text:return 'ELEBAR'
    if 'punto blu' in text or 'blu' in text:return 'BLU'
    return None
