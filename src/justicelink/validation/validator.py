"""
JusticeLink AI: Data Validation and Pipeline Module.
Implements integrity checks:
1. Schema & non-null enforcement
2. Date parsing and chronology verification (filing <= relevant_date)
3. Identifier regex format and uniqueness validation
4. Censoring consistency checks for pending vs disposed records
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np


@dataclass
class ValidationReport:
    total_records: int = 0
    duplicate_identifiers: int = 0
    null_counts: Dict[str, int] = field(default_factory=dict)
    invalid_dates: int = 0
    chronology_violations: int = 0
    censoring_inconsistencies: int = 0
    passed: bool = True
    errors: List[str] = field(default_factory=list)


class CaseDataValidator:
    """Validates raw case records against formal integrity rules."""

    IDENTIFIER_REGEX = re.compile(r"^KL-\d{6}-\d{4}$")
    VALID_STATUSES = {"Pending", "Disposed"}

    def validate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, ValidationReport]:
        report = ValidationReport(total_records=len(df))

        # Check required columns
        required_cols = {"filingnumber", "filing_date", "case_status", "relevant_date"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            report.passed = False
            report.errors.append(f"Missing required columns: {missing_cols}")
            return df, report

        # Null check
        for col in required_cols:
            null_count = int(df[col].isnull().sum())
            report.null_counts[col] = null_count
            if null_count > 0:
                report.passed = False
                report.errors.append(f"Column '{col}' has {null_count} null values.")

        # Duplicate check on identifiers
        duplicates = int(df["filingnumber"].duplicated().sum())
        report.duplicate_identifiers = duplicates
        if duplicates > 0:
            report.passed = False
            report.errors.append(f"Found {duplicates} duplicate filing identifiers.")

        # Identifier format check
        invalid_ids = (~df["filingnumber"].astype(str).str.match(self.IDENTIFIER_REGEX)).sum()
        if invalid_ids > 0:
            report.passed = False
            report.errors.append(f"Found {invalid_ids} invalid filingnumber strings.")

        # Status check
        unknown_status = (~df["case_status"].isin(self.VALID_STATUSES)).sum()
        if unknown_status > 0:
            report.passed = False
            report.errors.append(f"Found {unknown_status} unrecognised status values.")

        # Date parsing & Chronology check
        df_clean = df.copy()
        try:
            df_clean["filing_dt"] = pd.to_datetime(df_clean["filing_date"])
            df_clean["relevant_dt"] = pd.to_datetime(df_clean["relevant_date"])
        except Exception as e:
            report.passed = False
            report.errors.append(f"Date conversion error: {e}")
            return df_clean, report

        # Chronology: filing_dt <= relevant_dt
        violations = (df_clean["filing_dt"] > df_clean["relevant_dt"]).sum()
        report.chronology_violations = int(violations)
        if violations > 0:
            report.passed = False
            report.errors.append(f"{violations} cases have filing date after relevant date.")

        # Censoring check: all pending cases must share the same cutoff date
        pending_cases = df_clean[df_clean["case_status"] == "Pending"]
        if len(pending_cases) > 0:
            unique_cutoffs = pending_cases["relevant_dt"].nunique()
            if unique_cutoffs > 1:
                report.censoring_inconsistencies = unique_cutoffs
                report.errors.append(f"Pending cases have {unique_cutoffs} distinct cutoff dates.")

        return df_clean, report
