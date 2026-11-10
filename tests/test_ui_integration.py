"""
End-to-end integration and smoke tests for the redesigned Streamlit UI application and pages.
"""

import pytest
import pandas as pd


def test_ui_modules_importability():
    from justicelink.ui.theme import apply_theme, THEME_CSS
    from justicelink.ui.components import render_header, render_card, render_footer
    from justicelink.ui.components_3d import render_3d_court_building
    from justicelink.ui.pages import (
        p01_landing,
        p02_map,
        p03_analytics,
        p04_ml_lab,
        p05_ranking,
        p06_research,
    )

    assert p01_landing.render is not None
    assert p02_map.render is not None
    assert p03_analytics.render is not None
    assert p04_ml_lab.render is not None
    assert p05_ranking.render is not None
    assert p06_research.render is not None


def test_data_integrity_for_ui():
    # Parquet & CSV cleaned data
    df_clean = pd.read_parquet("data/processed/kollam_cases_cleaned.parquet")
    assert len(df_clean) == 1284
    assert (df_clean["duration_days"] >= 0).all()

    # Model metrics
    df_metrics = pd.read_csv("reports/model_benchmark_metrics.csv")
    assert len(df_metrics) == 7
    assert "Lasso Regression (alpha=0.5)" in df_metrics["model_name"].values

    # Ranked cases
    df_ranked = pd.read_csv("reports/pending_cases_ranked.csv")
    assert len(df_ranked) == 1006
    assert "rule_rank" in df_ranked.columns
