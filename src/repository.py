from __future__ import annotations
from pathlib import Path
import pandas as pd
from config.config import PROCESSED_DIR


def processed_path(brand: str) -> Path:
    slug = 'elebar' if brand == 'ELEBAR' else 'blu'
    return PROCESSED_DIR / slug / 'posts.parquet'


def load_processed(brand: str) -> pd.DataFrame:
    path=processed_path(brand)
    if not path.exists(): return pd.DataFrame()
    try: return pd.read_parquet(path)
    except Exception:
        csv=path.with_suffix('.csv')
        return pd.read_csv(csv) if csv.exists() else pd.DataFrame()


def save_processed(df: pd.DataFrame, brand: str):
    path=processed_path(brand); path.parent.mkdir(parents=True, exist_ok=True)
    try: df.to_parquet(path, index=False)
    except Exception: df.to_csv(path.with_suffix('.csv'), index=False)
