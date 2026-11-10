"""
JusticeLink AI: Ingestion & Feature Engineering Pipeline.
Transforms validated raw data into modeling-ready datasets:
- Extracts temporal components
- Calculates pendency & duration
- Distinguishes observed durations from censored durations
"""

from __future__ import annotations

import re
from pathlib import Path
import pandas as pd
import numpy as np

from justicelink.validation.validator import CaseDataValidator


def process_kollam_cases(
    raw_path: str | Path,
    output_dir: str | Path = "data/processed",
) -> pd.DataFrame:
    raw_path = Path(raw_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df_raw = pd.read_csv(raw_path)

    # 1. Validate
    validator = CaseDataValidator()
    df_val, report = validator.validate(df_raw)
    if not report.passed:
        raise ValueError(f"Validation failed with errors: {report.errors}")

    df = df_val.copy()

    # 2. Extract Identifier Features
    # Pattern KL-000004-2025 -> case_seq_no=4, filing_year_id=2025
    id_extracted = df["filingnumber"].str.extract(r"^KL-(\d{6})-(\d{4})$")
    df["case_seq_no"] = id_extracted[0].astype(int)
    df["filing_year_from_id"] = id_extracted[1].astype(int)

    # 3. Temporal Features
    df["filing_year"] = df["filing_dt"].dt.year
    df["filing_month"] = df["filing_dt"].dt.month
    df["filing_quarter"] = df["filing_dt"].dt.quarter
    df["filing_day_of_week"] = df["filing_dt"].dt.dayofweek
    df["filing_day_of_year"] = df["filing_dt"].dt.dayofyear

    # 4. Durations & Targets
    df["duration_days"] = (df["relevant_dt"] - df["filing_dt"]).dt.days
    df["is_disposed"] = (df["case_status"] == "Disposed").astype(int)

    # 5. Save processed data
    csv_out = output_dir / "kollam_cases_cleaned.csv"
    parquet_out = output_dir / "kollam_cases_cleaned.parquet"
    df.to_csv(csv_out, index=False)
    df.to_parquet(parquet_out, index=False)

    return df


if __name__ == "__main__":
    df = process_kollam_cases("data/raw/kerala/kollam_lifecycle_kaplanmeier.csv")
    print(f"Successfully processed {len(df)} records into data/processed/.")
