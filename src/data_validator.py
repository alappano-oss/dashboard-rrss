from __future__ import annotations
from dataclasses import dataclass, field
import pandas as pd
from config.config import REQUIRED_ANY, COLUMN_ALIASES

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _norm(s: str) -> str:
    return ''.join(ch for ch in str(s).strip().lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n') if ch.isalnum() or ch == '_')


def resolve_columns(columns) -> dict[str,str]:
    normalized = {_norm(c): c for c in columns}
    mapping = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            key = _norm(alias)
            if key in normalized:
                mapping[canonical] = normalized[key]
                break
    return mapping


def validate_raw(df: pd.DataFrame) -> ValidationResult:
    errors, warnings = [], []
    mapping = resolve_columns(df.columns)
    for required, aliases in REQUIRED_ANY.items():
        if required not in mapping:
            errors.append(f'Falta una columna de {required}: se esperaba alguna de {aliases}.')
    if df.empty:
        errors.append('El archivo no contiene registros.')
    if 'date' in mapping:
        parsed = pd.to_datetime(df[mapping['date']], errors='coerce', dayfirst=True)
        bad = int(parsed.isna().sum())
        if bad: warnings.append(f'{bad} registros tienen una fecha no interpretable.')
    if df.duplicated().sum(): warnings.append(f'Se detectaron {int(df.duplicated().sum())} filas idénticas.')
    return ValidationResult(not errors, errors, warnings)
