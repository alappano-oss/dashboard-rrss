from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from config.config import (
    CANONICAL_COLUMNS,
    FORMAT_MAP,
    NUMERIC_COLUMNS,
    PLATFORM_MAP,
)
from src.data_validator import resolve_columns

def normalize_format(value):
    if pd.isna(value):
        return pd.NA

    raw = str(value).strip().lower()

    if raw in FORMAT_MAP:
        return FORMAT_MAP[raw]

    if "reel" in raw:
        return "Reel"

    if "carrusel" in raw or "carousel" in raw:
        return "Carrusel"

    if "video" in raw:
        return "Video"

    if (
        "image" in raw
        or "imagen" in raw
        or "photo" in raw
        or "foto" in raw
    ):
        return "Imagen"

    if "post" in raw:
        return "Post"

    return str(value).strip()


def normalize_platform(value):
    if pd.isna(value):
        return pd.NA

    raw = str(value).strip().lower()

    return PLATFORM_MAP.get(raw, str(value).strip())


def infer_platform_from_filename(filename: str):
    """
    Meta suele exportar archivos con prefijos:
    FB- = Facebook
    IG- = Instagram
    """
    filename_upper = str(filename).upper()

    if filename_upper.startswith("FB-"):
        return "Facebook"

    if filename_upper.startswith("IG-"):
        return "Instagram"

    return pd.NA


def _to_number(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")

    def parse(value):
        if pd.isna(value):
            return pd.NA

        s = str(value).strip().replace(" ", "")

        if not s:
            return pd.NA

        if "," in s and "." in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")

        elif "," in s:
            tail = s.rsplit(",", 1)[1]

            if len(tail) in (1, 2):
                s = s.replace(",", ".")
            else:
                s = s.replace(",", "")

        elif s.count(".") > 1:
            s = s.replace(".", "")

        try:
            return float(s)
        except ValueError:
            return pd.NA

    return series.map(parse).astype("Float64")


def _stable_key(row: pd.Series) -> str:
    if pd.notna(row.get("post_id")) and str(row.get("post_id")).strip():
        return "id:" + str(row["post_id"]).strip()

    parts = [
        str(row.get(k, ""))
        for k in [
            "brand",
            "platform",
            "account",
            "date",
            "time",
            "url",
            "copy",
        ]
    ]

    return (
        "hash:"
        + hashlib.sha1(
            "|".join(parts).encode("utf-8", errors="ignore")
        ).hexdigest()
    )


def normalize_dataframe(
    raw: pd.DataFrame,
    filename: str,
    brand: str,
) -> pd.DataFrame:

    mapping = resolve_columns(raw.columns)

    out = pd.DataFrame(index=raw.index)

    for canonical in CANONICAL_COLUMNS:
        source = mapping.get(canonical)

        if source:
            out[canonical] = raw[source]
        else:
            out[canonical] = pd.NA

    out["brand"] = brand
    out["source_file"] = filename
    out["source_row"] = np.arange(1, len(out) + 1)

    if "date" in mapping:
        date_values = raw[mapping["date"]]

        out["date"] = pd.to_datetime(
            date_values,
            errors="coerce",
            dayfirst=False,
        ).dt.date

    else:
        out["date"] = pd.NaT

    if "time" in mapping:
        time_values = raw[mapping["time"]].astype("string")

        parsed_datetime = pd.to_datetime(
            time_values,
            errors="coerce",
            dayfirst=False,
        )

        out["time"] = parsed_datetime.dt.strftime("%H:%M:%S")

        out["time"] = out["time"].astype("string")

    else:
        out["time"] = pd.NA
    if "platform" in mapping:
        out["platform"] = out["platform"].map(normalize_platform)
    else:
        out["platform"] = infer_platform_from_filename(filename)

    if "format" in mapping:
        out["format"] = out["format"].map(normalize_format)

    for column in NUMERIC_COLUMNS:
        if column in out.columns:
            out[column] = _to_number(out[column])


    interaction_columns = [
        column
        for column in [
            "likes",
            "comments",
            "shares",
            "saves",
        ]
        if column in out.columns
    ]

    if interaction_columns:
        derived_interactions = out[interaction_columns].sum(
            axis=1,
            min_count=1,
        )

        if "interactions" in out.columns:
            out["interactions"] = out["interactions"].where(
                out["interactions"].notna(),
                derived_interactions,
            )
        else:
            out["interactions"] = derived_interactions

    out["er_reach"] = np.where(
        out["reach"].notna()
        & out["interactions"].notna()
        & (out["reach"] != 0),
        out["interactions"] / out["reach"] * 100,
        np.nan,
    )

    # ---------------------------------------------------------
    # ENGAGEMENT RATE POR IMPRESIONES
    # ---------------------------------------------------------

    out["er_impressions"] = np.where(
        out["impressions"].notna()
        & out["interactions"].notna()
        & (out["impressions"] != 0),
        out["interactions"] / out["impressions"] * 100,
        np.nan,
    )

    out["_record_key"] = out.apply(
        _stable_key,
        axis=1,
    )

    return out


def deduplicate(
    existing: pd.DataFrame,
    incoming: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:

    if existing is None or existing.empty:
        combined = incoming.copy()
    else:
        combined = pd.concat(
            [existing, incoming],
            ignore_index=True,
        )

    before = len(combined)

    combined = combined.drop_duplicates(
        subset=["_record_key"],
        keep="first",
    )

    duplicates = before - len(combined)

    return combined, duplicates
