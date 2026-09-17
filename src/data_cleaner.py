from __future__ import annotations
from pathlib import Path
import hashlib
import pandas as pd
import numpy as np
from config.config import CANONICAL_COLUMNS, COLUMN_ALIASES, FORMAT_MAP, PLATFORM_MAP, NUMERIC_COLUMNS
from src.data_validator import resolve_columns


def normalize_format(value):
    if pd.isna(value): return pd.NA
    raw = str(value).strip().lower()
    if raw in FORMAT_MAP: return FORMAT_MAP[raw]
    if 'reel' in raw: return 'Reel'
    if 'carrusel' in raw or 'carousel' in raw: return 'Carrusel'
    if 'video' in raw: return 'Video'
    if 'image' in raw or 'imagen' in raw or 'photo' in raw: return 'Imagen'
    if 'post' in raw: return 'Post'
    return str(value).strip()


def normalize_platform(value):
    if pd.isna(value): return pd.NA
    raw = str(value).strip().lower()
    return PLATFORM_MAP.get(raw, str(value).strip())


def _to_number(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors='coerce')

    def parse(value):
        if pd.isna(value): return pd.NA
        s = str(value).strip().replace(' ', '')
        if not s: return pd.NA
        # Support common Meta/Spanish exports: 1.234,56; 1234,56; 1,234.56.
        if ',' in s and '.' in s:
            if s.rfind(',') > s.rfind('.'):
                s = s.replace('.', '').replace(',', '.')
            else:
                s = s.replace(',', '')
        elif ',' in s:
            tail = s.rsplit(',', 1)[1]
            s = s.replace(',', '.') if len(tail) in (1,2) else s.replace(',', '')
        elif s.count('.') > 1:
            s = s.replace('.', '')
        try: return float(s)
        except ValueError: return pd.NA
    return series.map(parse).astype('Float64')


def _stable_key(row: pd.Series) -> str:
    if pd.notna(row.get('post_id')) and str(row.get('post_id')).strip():
        return 'id:' + str(row['post_id']).strip()
    parts = [str(row.get(k,'')) for k in ['brand','platform','account','date','time','url','copy']]
    return 'hash:' + hashlib.sha1('|'.join(parts).encode('utf-8', errors='ignore')).hexdigest()


def normalize_dataframe(raw: pd.DataFrame, filename: str, brand: str) -> pd.DataFrame:
    mapping = resolve_columns(raw.columns)
    out = pd.DataFrame(index=raw.index)
    for canonical in CANONICAL_COLUMNS:
        source = mapping.get(canonical)
        out[canonical] = raw[source] if source else pd.NA
    out['brand'] = brand
    out['source_file'] = filename
    out['source_row'] = np.arange(1, len(out)+1)
    out['date'] = pd.to_datetime(out['date'], errors='coerce', dayfirst=True).dt.date
    out['time'] = out['time'].astype('string').replace({'<NA>': pd.NA})
    out['platform'] = out['platform'].map(normalize_platform)
    out['format'] = out['format'].map(normalize_format)
    for c in NUMERIC_COLUMNS:
        out[c] = _to_number(out[c])
    derived_interactions = out[['likes','comments','shares','saves']].sum(axis=1, min_count=1)
    out['interactions'] = out['interactions'].where(out['interactions'].notna(), derived_interactions)
    out['er_reach'] = np.where(out['reach'].notna() & out['interactions'].notna() & (out['reach'] != 0), out['interactions']/out['reach']*100, np.nan)
    out['er_impressions'] = np.where(out['impressions'].notna() & out['interactions'].notna() & (out['impressions'] != 0), out['interactions']/out['impressions']*100, np.nan)
    out['_record_key'] = out.apply(_stable_key, axis=1)
    return out


def deduplicate(existing: pd.DataFrame, incoming: pd.DataFrame) -> tuple[pd.DataFrame,int]:
    if existing is None or existing.empty:
        combined = incoming.copy()
    else:
        combined = pd.concat([existing, incoming], ignore_index=True)
    before = len(combined)
    combined = combined.drop_duplicates(subset=['_record_key'], keep='first')
    return combined, before - len(combined)
