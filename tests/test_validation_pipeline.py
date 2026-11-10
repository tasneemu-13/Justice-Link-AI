import pytest
import pandas as pd
from justicelink.validation.validator import CaseDataValidator
from justicelink.ingestion.pipeline import process_kollam_cases


def test_validator_on_raw_data():
    raw_df = pd.read_csv("data/raw/kerala/kollam_lifecycle_kaplanmeier.csv")
    validator = CaseDataValidator()
    df_clean, report = validator.validate(raw_df)

    assert report.passed is True
    assert report.total_records == 1284
    assert report.duplicate_identifiers == 0
    assert report.chronology_violations == 0
    assert len(report.errors) == 0


def test_pipeline_processing(tmp_path):
    df_processed = process_kollam_cases(
        "data/raw/kerala/kollam_lifecycle_kaplanmeier.csv",
        output_dir=tmp_path,
    )

    assert len(df_processed) == 1284
    assert "duration_days" in df_processed.columns
    assert "is_disposed" in df_processed.columns
    assert "filing_month" in df_processed.columns
    assert (df_processed["duration_days"] >= 0).all()
    assert (tmp_path / "kollam_cases_cleaned.csv").exists()
