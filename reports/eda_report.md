# Exploratory Data Analysis & Empirical Case Survival Report

**Project:** JusticeLink AI  
**Scope:** Kerala District Courts (Kollam Case Lifecycle Dataset)  
**Date:** 2026-11-09  

---

## 1. Executive Summary

An exploratory empirical investigation was conducted on **1,284 verified judicial case records** originating from the Kollam judicial district under the digital ONCourts initiative (Section 138, Negotiable Instruments Act).

### Key Empirical Findings:
- **Case Status Composition:**
  - **Pending:** 1,006 cases (78.35%)
  - **Disposed:** 278 cases (21.65%)
- **Disposal Duration (Completed Cases):**
  - **Mean Duration:** 166.2 days (~5.5 months)
  - **Median Duration:** 149.5 days (~5.0 months)
  - **Standard Deviation:** 104.7 days
  - **Interquartile Range (IQR):** 158.0 days (Q1 = 76.0 days, Q3 = 234.0 days)
  - **Minimum to Maximum:** 15 days to 455 days
  - **Skewness:** +0.64 (moderate right-skew, standard for judicial duration data where most cases resolve moderately quickly but procedural delays create a long tail).
- **Censoring Cutoff Analysis:**
  - 100% of pending cases are observed up to **March 10, 2026**, with an observed age between 0 and 475 days.
  - The mean age of pending cases is 181.8 days, which reflects active processing and newer case arrivals.

---

## 2. Visualizations and Empirical Distributions

### Figure 1: Status Distribution & Observed Duration
![Status and Duration](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/figures/fig1_status_and_duration.png)
- Illustrates the proportion of pending vs. disposed cases.
- Side-by-side boxplot contrasts the completed lifecycle distribution (disposed) against the censored age distribution (pending).

### Figure 2: Disposal Duration Distribution
![Disposal Duration](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/figures/fig2_disposal_duration_hist.png)
- Displays unimodal distribution peaking between 90 and 180 days.
- Mean (166.2 days) sits slightly to the right of Median (149.5 days), reflecting the influence of extended trial durations.

### Figure 3: Monthly Filing Inflow Trends
![Filing Trends](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/figures/fig3_filing_trends.png)
- Tracks monthly case filing velocity across 2024, 2025, and early 2026.
- Highlights clear cohort effects: earlier cohorts (2024–early 2025) account for the majority of disposed cases, while late 2025 and 2026 filings represent active, pending matters.

### Figure 4: Non-Parametric Kaplan-Meier Survival Function
![Kaplan-Meier Survival](file:///c:/Users/Tasneem/OneDrive/Desktop/JusticeLink%20AI/reports/figures/fig4_kaplan_meier_survival.png)
- Evaluates the probability $S(t) = P(T > t)$ of a case remaining pending beyond $t$ days without assuming parametric normality.
- Accurately adjusts for right-censoring among active cases.

---

## 3. Modeling Implications for Machine Learning (Milestone 3)

1. **Target Formulation for Regression (Stage A):**
   - The numerical regression target is **`duration_days` for disposed cases ($N=278$)**.
   - Pending cases must not be labeled with their current age as their final disposal duration, to prevent severe negative bias / data leakage.
2. **Feature Candidate Space:**
   - Temporal indicators: `filing_month`, `filing_quarter`, `filing_day_of_week`, `filing_day_of_year`.
   - Inflow / Queue velocity indicators: `case_seq_no` (the chronological sequence index of filing).
3. **Model Selection Sequence:**
   - Baseline: Mean / Median regressor.
   - Linear Regression: Establishing interpretability and feature coefficients.
   - Regularized Regression: Ridge and Lasso to penalize multicollinearity.
   - Decision Tree Regressor: Capturing non-linear threshold effects.
   - Random Forest Regressor: Quantifying non-linear feature interactions and ensemble stability.
