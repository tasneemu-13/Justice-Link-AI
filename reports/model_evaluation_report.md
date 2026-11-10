# Model Evaluation & Benchmark Comparison Report

**Project:** JusticeLink AI  
**Dataset:** Kerala District Court (Kollam Case Lifecycle Dataset)  
**Task:** Case Duration Estimation from Filing to Disposal (Disposed Cases, $N=278$)  
**Validation Strategy:** 80/20 Independent Train/Test Split (Random Seed 42) + 5-Fold Cross-Validation  
**Date:** 2026-11-09  

---

## 1. Regression Model Comparison Table

| Model | Test MAE (Days) | Test RMSE (Days) | Test $R^2$ Score | 5-Fold CV MAE (Mean ± Std) | Model Complexity & Key Parameters |
|:---|:---:|:---:|:---:|:---:|:---|
| **Baseline (Mean)** | 85.24 | 99.48 | -0.001 | 88.47 ± 7.92 | Empirical Mean Predictor (166.2 days) |
| **Baseline (Median)** | 83.71 | 99.89 | -0.010 | 88.52 ± 8.11 | Empirical Median Predictor (149.5 days) |
| **Linear Regression (OLS)** | 64.47 | 81.01 | 0.336 | 68.84 ± 7.21 | Standardized coefficients |
| **Ridge Regression** | 63.61 | 80.61 | 0.343 | 67.98 ± 7.05 | $L_2$ Regularization ($\alpha=1.0$) |
| **Lasso Regression** | **63.49** | **80.58** | **0.343** | **67.94 ± 7.02** | $L_1$ Regularization ($\alpha=0.5$) |
| **Decision Tree Regressor** | 66.55 | 83.03 | 0.302 | 74.10 ± 9.15 | `max_depth=4`, `min_samples_leaf=5` |
| **Random Forest Regressor** | 67.18 | 83.84 | 0.289 | 71.05 ± 7.85 | `n_estimators=100`, `max_depth=5` |

---

## 2. In-Depth Comparative Analysis

1. **Improvement Over Baselines:**
   - Both linear and ensemble models demonstrate a substantial improvement over the naive mean/median baselines.
   - Test MAE dropped from **85.24 days** (Baseline) to **63.49 days** (Lasso Regression), representing an error reduction of over **25.5%** (~21.7 days).
   - Test $R^2$ achieved **0.343**, demonstrating that temporal and queue arrival dynamics account for over one-third of the total variance in case disposition times.

2. **Why Regularized Linear Models Outperformed Ensembles:**
   - On this focused dataset of 278 completed cases, **Ridge and Lasso Regression** delivered the lowest test error (63.49–63.61 days) and the most stable 5-fold cross-validation scores (~67.9 days).
   - Because tree-based regressors (Decision Trees and Random Forests) make orthogonal step-function cuts, they can slightly overfit small sample sizes. Lasso’s continuous shrinkage effectively constrained collinear calendar variables (`filing_month` vs. `filing_day_of_year`).

3. **Residual Diagnostics & Actual vs. Predicted Performance:**
   - Visual inspection in [`fig5_regression_actual_vs_predicted.png`](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/figures/fig5_regression_actual_vs_predicted.png) shows that predictions cluster appropriately along the $y=x$ trajectory for cases resolving between 60 and 240 days.
   - For cases experiencing exceptional delays (>350 days), predictions are conservative, reflecting the statistical limit of predicting procedural anomalies purely from filing-time metadata without real-time hearing notes.

---

## 3. Explainability & Feature Influence

Based on the Gini importances and standardized coefficients:
- **`case_seq_no` (Queue Sequence / Inflow Position):** Most influential feature in non-linear models (accounting for **76.9%** of Random Forest feature importance and **84.8%** of Decision Tree splits). Demonstrates that cases filed earlier in a yearly cycle experience longer total calendar exposure compared to late-cycle filings.
- **`filing_day_of_year` & `filing_year`:** Primary drivers of temporal trend, capturing procedural shifts and docket clearance cycles.
- Feature importance visualization available in [`fig6_feature_importances.png`](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/figures/fig6_feature_importances.png).

---

## 4. Explainable Case Ranking (Procedural Review Queue)

For pending matters ($N=1,006$), an explainable ranking engine was implemented in [`ranker.py`](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/src/justicelink/ranking/ranker.py):
- **Objective:** Triage cases requiring administrative or procedural review to prevent unmonitored pendency accumulation.
- **Rule-Based vs. ML Priority Concordance:**
  - Top-50 Concordance Precision: **46.0%**.
  - All top-ranked cases provide an inspectable audit string (e.g., observed pendency days, filing cohort, queue sequence, and normalized procedural score).
  - Sample case ranking explanations exported to [`reports/top_100_ranking_explanations.json`](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/top_100_ranking_explanations.json).
