from __future__ import annotations
from pathlib import Path
import re
import pandas as pd


def read_csv(path_or_buffer) -> pd.DataFrame:
    """Read Meta CSV with delimiter/encoding fallbacks; never silently drops columns."""
    attempts = [
        {'encoding':'utf-8-sig', 'sep':','},
        {'encoding':'utf-8', 'sep':','},
        {'encoding':'latin1', 'sep':','},
        {'encoding':'utf-8-sig', 'sep':';'},
        {'encoding':'latin1', 'sep':';'},
    ]
    errors = []
    for kwargs in attempts:
        try:
            df = pd.read_csv(path_or_buffer, **kwargs)
            if len(df.columns) > 1:
                return df
        except Exception as exc:
            errors.append(str(exc))
    raise ValueError('No se pudo leer el CSV. Verificá encoding y delimitador. ' + ' | '.join(errors[-2:]))


def infer_brand(filename: str, dataframe: pd.DataFrame | None = None) -> str | None:
    text = filename.lower()
    if any(x in text for x in ['elebar','tarjeta elebar']): return 'ELEBAR'
    if any(x in text for x in ['blu','punto blu','puntoblu']): return 'PUNTO BLU'
    if dataframe is not None:
        values = ' '.join(map(str, dataframe.astype(str).head(100).values.flatten())).lower()
        if 'elebar' in values: return 'ELEBAR'
        if 'punto blu' in values or 'puntoblu' in values: return 'PUNTO BLU'
    return None


def infer_period(filename: str, dataframe: pd.DataFrame | None = None) -> tuple[str|None,str|None]:
    """Return start/end dates inferred from date column where possible."""
    if dataframe is not None:
        for c in dataframe.columns:
            if any(k in str(c).lower() for k in ['date','fecha','published']):
                parsed = pd.to_datetime(dataframe[c], errors='coerce', dayfirst=True)
                if parsed.notna().any():
                    return parsed.min().date().isoformat(), parsed.max().date().isoformat()
    m = re.search(r'(20\d{2})[-_](\d{1,2})', filename)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        p = pd.Period(f'{y}-{mo:02d}', freq='M')
        return p.start_time.date().isoformat(), p.end_time.date().isoformat()
    return None, None
