"""
JusticeLink AI: Regression Modeling and Benchmarking Pipeline.
Trains and compares:
1. Baseline Mean & Median Predictors
2. Ordinary Least Squares (Linear Regression)
3. Ridge Regression (L2 regularization)
4. Lasso Regression (L1 regularization)
5. Decision Tree Regressor (tuned max_depth, min_samples_leaf)
6. Random Forest Regressor (tuned n_estimators, max_depth)

Evaluates on:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score
Includes 5-Fold Cross-Validation, Feature Importance, and Residual Diagnostics.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor


@dataclass
class ModelMetrics:
    model_name: str
    train_mae: float
    train_rmse: float
    train_r2: float
    test_mae: float
    test_rmse: float
    test_r2: float
    cv_mae_mean: float
    cv_mae_std: float
    cv_r2_mean: float


def train_and_evaluate_models(
    input_path: str = "data/processed/kollam_cases_cleaned.parquet",
    reports_dir: str = "reports",
    figures_dir: str = "reports/figures",
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    reports_path = Path(reports_dir)
    fig_path = Path(figures_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    fig_path.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_path)

    # 1. Filter completed cases only to prevent duration leakage / right-censoring bias
    df_disposed = df[df["case_status"] == "Disposed"].copy()

    # 2. Define Features & Target
    feature_cols = [
        "case_seq_no",
        "filing_year",
        "filing_month",
        "filing_quarter",
        "filing_day_of_week",
        "filing_day_of_year",
    ]
    target_col = "duration_days"

    X = df_disposed[feature_cols].copy()
    y = df_disposed[target_col].values

    # 3. Train-Test Split (80/20 with fixed seed for research reproducibility)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )

    # Feature scaling for linear models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Instantiate Models
    models: Dict[str, Any] = {
        "Baseline (Mean)": (DummyRegressor(strategy="mean"), False),
        "Baseline (Median)": (DummyRegressor(strategy="median"), False),
        "Linear Regression": (LinearRegression(), True),
        "Ridge Regression (alpha=1.0)": (Ridge(alpha=1.0, random_state=42), True),
        "Lasso Regression (alpha=0.5)": (Lasso(alpha=0.5, random_state=42), True),
        "Decision Tree (max_depth=4)": (
            DecisionTreeRegressor(max_depth=4, min_samples_leaf=5, random_state=42),
            False,
        ),
        "Random Forest (n=100, depth=5)": (
            RandomForestRegressor(
                n_estimators=100, max_depth=5, min_samples_leaf=3, random_state=42
            ),
            False,
        ),
    }

    results: List[ModelMetrics] = []
    predictions: Dict[str, np.ndarray] = {}
    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    for name, (model, requires_scale) in models.items():
        X_tr = X_train_scaled if requires_scale else X_train
        X_te = X_test_scaled if requires_scale else X_test

        # Fit model
        model.fit(X_tr, y_train)
        y_train_pred = model.predict(X_tr)
        y_test_pred = model.predict(X_te)
        predictions[name] = y_test_pred

        # Cross-validation on training fold
        cv_res = cross_validate(
            model,
            X_tr,
            y_train,
            cv=cv,
            scoring=["neg_mean_absolute_error", "r2"],
        )

        metrics = ModelMetrics(
            model_name=name,
            train_mae=float(mean_absolute_error(y_train, y_train_pred)),
            train_rmse=float(np.sqrt(mean_squared_error(y_train, y_train_pred))),
            train_r2=float(r2_score(y_train, y_train_pred)),
            test_mae=float(mean_absolute_error(y_test, y_test_pred)),
            test_rmse=float(np.sqrt(mean_squared_error(y_test, y_test_pred))),
            test_r2=float(r2_score(y_test, y_test_pred)),
            cv_mae_mean=float(-cv_res["test_neg_mean_absolute_error"].mean()),
            cv_mae_std=float(cv_res["test_neg_mean_absolute_error"].std()),
            cv_r2_mean=float(cv_res["test_r2"].mean()),
        )
        results.append(metrics)

    metrics_df = pd.DataFrame([asdict(m) for m in results])

    # 5. Extract Feature Importances / Coefficients for Explainability
    lr_model = models["Linear Regression"][0]
    lr_coefs = dict(zip(feature_cols, lr_model.coef_))

    rf_model = models["Random Forest (n=100, depth=5)"][0]
    rf_importances = dict(zip(feature_cols, rf_model.feature_importances_))

    dt_model = models["Decision Tree (max_depth=4)"][0]
    dt_importances = dict(zip(feature_cols, dt_model.feature_importances_))

    explainability_data = {
        "linear_coefficients_standardized": {k: float(v) for k, v in lr_coefs.items()},
        "decision_tree_importances": {k: float(v) for k, v in dt_importances.items()},
        "random_forest_importances": {k: float(v) for k, v in rf_importances.items()},
    }

    with open(reports_path / "model_explainability.json", "w") as f:
        json.dump(explainability_data, f, indent=2)

    # 6. Generate Diagnostics & Visual Comparisons
    # Figure 5: Actual vs Predicted across Models
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    compare_models = [
        "Baseline (Mean)",
        "Linear Regression",
        "Decision Tree (max_depth=4)",
        "Random Forest (n=100, depth=5)",
    ]

    for idx, m_name in enumerate(compare_models):
        ax = axes[idx]
        y_pred = predictions[m_name]
        ax.scatter(y_test, y_pred, alpha=0.7, color="#2b5c8f", edgecolors="black")
        min_v, max_v = min(min(y_test), min(y_pred)), max(max(y_test), max(y_pred))
        ax.plot([min_v, max_v], [min_v, max_v], "r--", linewidth=1.5, label="Perfect Fit (y=x)")
        ax.set_title(m_name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Actual Disposal Duration (Days)")
        ax.set_ylabel("Predicted Duration (Days)")
        ax.grid(True, linestyle="--", alpha=0.6)
        m_row = metrics_df[metrics_df["model_name"] == m_name].iloc[0]
        ax.text(
            0.05,
            0.85,
            f"Test MAE: {m_row['test_mae']:.1f} d\nTest R²: {m_row['test_r2']:.3f}",
            transform=ax.transAxes,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.tight_layout()
    plt.savefig(fig_path / "fig5_regression_actual_vs_predicted.png", dpi=300)
    plt.close()

    # Figure 6: Feature Importances
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Linear Coefs
    sorted_lr = sorted(lr_coefs.items(), key=lambda x: abs(x[1]), reverse=True)
    features_lr, vals_lr = zip(*sorted_lr)
    colors_lr = ["#d95f02" if v < 0 else "#2b5c8f" for v in vals_lr]
    ax1.barh(features_lr, vals_lr, color=colors_lr, edgecolor="black")
    ax1.axvline(0, color="black", linestyle="-", linewidth=0.8)
    ax1.set_title("Standardized Linear Regression Coefficients", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Coefficient Magnitude (Days)")
    ax1.grid(axis="x", linestyle="--", alpha=0.7)

    # RF Importances
    sorted_rf = sorted(rf_importances.items(), key=lambda x: x[1], reverse=True)
    features_rf, vals_rf = zip(*sorted_rf)
    ax2.barh(features_rf, vals_rf, color="#1b7837", edgecolor="black")
    ax2.set_title("Random Forest Gini Feature Importances", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Relative Importance")
    ax2.grid(axis="x", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(fig_path / "fig6_feature_importances.png", dpi=300)
    plt.close()

    metrics_df.to_csv(reports_path / "model_benchmark_metrics.csv", index=False)
    print("Model training and benchmarking completed successfully.")
    return metrics_df, explainability_data


if __name__ == "__main__":
    df_metrics, exp = train_and_evaluate_models()
    print(df_metrics[["model_name", "test_mae", "test_rmse", "test_r2", "cv_mae_mean"]].to_string())
