from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_loader import read_csv, infer_brand
from src.data_validator import validate_raw
from src.data_cleaner import normalize_dataframe, deduplicate
from src.repository import load_processed, save_processed


def ingest_files(files, forced_brand: str | None = None) -> dict:
    result = {
        "files_processed": 0,
        "new_records": 0,
        "duplicates": 0,
        "rejected": 0,
        "errors": [],
        "warnings": [],
    }

    by_brand = {}

    for file in files:
        name = getattr(file, "name", None)

        if not name:
            name = Path(str(file)).name

        try:
            raw = read_csv(file)

            validation = validate_raw(raw)

            result["warnings"] += [
                f"{name}: {w}" for w in validation.warnings
            ]

            if not validation.valid:
                result["rejected"] += 1
                result["errors"] += [
                    f"{name}: {e}" for e in validation.errors
                ]
                continue

            brand = forced_brand or infer_brand(name, raw)

            if brand is None:
                result["rejected"] += 1
                result["errors"].append(
                    f"{name}: no se pudo identificar la marca automáticamente."
                )
                continue

            clean = normalize_dataframe(raw, name, brand)

            by_brand.setdefault(brand, []).append(clean)

            result["files_processed"] += 1

        except Exception as exc:
            result["rejected"] += 1
            result["errors"].append(f"{name}: {exc}")

    for brand, frames in by_brand.items():
        incoming = pd.concat(frames, ignore_index=True)

        existing = load_processed(brand)

        combined, dups = deduplicate(existing, incoming)

        result["duplicates"] += dups
        result["new_records"] += len(combined) - len(existing)

        save_processed(combined, brand)

    return result


def ingest_raw_directory(brand: str) -> dict:
    from config.config import RAW_DIR

    folder = RAW_DIR / ("elebar" if brand == "ELEBAR" else "blu")

    files = sorted(folder.glob("*.csv"))

    if not files:
        return {
            "files_processed": 0,
            "new_records": 0,
            "duplicates": 0,
            "rejected": 0,
            "errors": [f"No hay CSV en {folder}."],
            "warnings": [],
        }

    return ingest_files(files, forced_brand=brand)
