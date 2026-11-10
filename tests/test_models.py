"""
Unit tests for the regression modeling pipeline.
"""

import pytest
import pandas as pd
from justicelink.models.regression import train_and_evaluate_models


def test_regression_pipeline_execution(tmp_path):
    metrics_df, explainability = train_and_evaluate_models(
        input_path="data/processed/kollam_cases_cleaned.parquet",
        reports_dir=tmp_path / "reports",
        figures_dir=tmp_path / "figures",
    )

    assert len(metrics_df) == 7
    assert "Linear Regression" in metrics_df["model_name"].values
    assert "Random Forest (n=100, depth=5)" in metrics_df["model_name"].values
    
    # Models must outperform dummy baselines on MAE
    baseline_mae = metrics_df[metrics_df["model_name"] == "Baseline (Mean)"]["test_mae"].iloc[0]
    lasso_mae = metrics_df[metrics_df["model_name"] == "Lasso Regression (alpha=0.5)"]["test_mae"].iloc[0]
    assert lasso_mae < baseline_mae

    # Check explainability exports
    assert "linear_coefficients_standardized" in explainability
    assert "random_forest_importances" in explainability
