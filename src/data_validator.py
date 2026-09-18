from dataclasses import dataclass,field
import re,pandas as pd
from config.config import ALIASES
@dataclass
class ValidationResult:
    valid:bool; errors:list[str]=field(default_factory=list); warnings:list[str]=field(default_factory=list)
def norm(v):return re.sub(r'[^a-z0-9]+','',str(v).strip().lower().translate(str.maketrans('áéíóúüñ','aeiouun')))
def resolve_columns(columns):
    normalized={norm(c):c for c in columns}; m={}
    for k,aliases in ALIASES.items():
        for a in aliases:
            if norm(a) in normalized:m[k]=normalized[norm(a)];break
    return m
def validate_raw(df):
    errors=[];warnings=[]
    if df.empty:return ValidationResult(False,['El archivo no contiene registros.'],[])
    m=resolve_columns(df.columns)
    if 'post_id' not in m and 'url' not in m:errors.append('No se encontró identificador de publicación ni enlace permanente.')
    if 'published_datetime' not in m:errors.append("No se encontró 'Hora de publicación', necesaria para determinar la fecha.")
    if 'reach' not in m:warnings.append('No se encontró Alcance.')
    if 'interactions' not in m and not any(k in m for k in ('likes','comments','shares','saves')):warnings.append('No se encontraron métricas de interacción.')
    return ValidationResult(not errors,errors,warnings)
