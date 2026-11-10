"""
JusticeLink AI: Exploratory Data Analysis & Visualization Script.
Pure Matplotlib & NumPy/Pandas implementation (no dependency on seaborn).
Analyzes:
1. Case status distribution (Pending vs Disposed)
2. Case duration and pendency distribution
3. Monthly and quarterly filing trends
4. Non-parametric Kaplan-Meier survival curves for judicial resolution
Generates high-resolution publication-quality plots in reports/figures/.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def run_eda(
    input_path: str = "data/processed/kollam_cases_cleaned.parquet",
    output_fig_dir: str = "reports/figures",
    output_stats_path: str = "reports/eda_summary_metrics.json",
):
    fig_dir = Path(output_fig_dir)
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_path)
    df["filing_dt"] = pd.to_datetime(df["filing_dt"])
    df["relevant_dt"] = pd.to_datetime(df["relevant_dt"])

    # 1. Figure 1: Status Distribution & Duration Boxplot
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    status_counts = df["case_status"].value_counts()
    axes[0].bar(status_counts.index, status_counts.values, color=["#2b5c8f", "#d95f02"], edgecolor="black")
    axes[0].set_title("Case Distribution by Status", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Number of Cases")
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)
    for i, v in enumerate(status_counts.values):
        axes[0].text(i, v + 15, f"{v} ({v/len(df)*100:.1f}%)", ha="center", fontweight="bold")

    disposed_durations = df[df["case_status"] == "Disposed"]["duration_days"]
    pending_durations = df[df["case_status"] == "Pending"]["duration_days"]
    
    bplot = axes[1].boxplot(
        [pending_durations, disposed_durations],
        labels=["Pending (Censored Age)", "Disposed (Duration)"],
        patch_artist=True,
        medianprops=dict(color="black", linewidth=1.5),
    )
    colors = ["#2b5c8f", "#d95f02"]
    for patch, color in zip(bplot["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    axes[1].set_title("Observed Duration / Age (Days) by Status", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Duration in Days")
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    fig1_path = fig_dir / "fig1_status_and_duration.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()

    # 2. Figure 2: Disposed Case Duration Distribution (Histogram)
    disposed = df[df["case_status"] == "Disposed"]
    fig, ax = plt.subplots(figsize=(8, 5))
    counts, bins, patches = ax.hist(disposed["duration_days"], bins=25, color="#2b5c8f", edgecolor="black", alpha=0.85)
    ax.axvline(disposed["duration_days"].median(), color="red", linestyle="--", linewidth=2, label=f"Median: {disposed['duration_days'].median():.0f} days")
    ax.axvline(disposed["duration_days"].mean(), color="black", linestyle=":", linewidth=2, label=f"Mean: {disposed['duration_days'].mean():.1f} days")
    ax.set_title("Distribution of Case Disposal Duration (Completed Cases)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Disposal Duration (Days)")
    ax.set_ylabel("Number of Cases")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend(frameon=True)

    plt.tight_layout()
    fig2_path = fig_dir / "fig2_disposal_duration_hist.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()

    # 3. Figure 3: Filing Trend Over Time (Monthly Filings)
    df["filing_year_month"] = df["filing_dt"].dt.to_period("M").dt.to_timestamp()
    monthly_counts = df.groupby(["filing_year_month", "case_status"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    months = [d.strftime("%b %Y") for d in monthly_counts.index]
    x = np.arange(len(months))
    p1 = ax.bar(x, monthly_counts.get("Disposed", 0), label="Disposed", color="#d95f02", edgecolor="black")
    p2 = ax.bar(x, monthly_counts.get("Pending", 0), bottom=monthly_counts.get("Disposed", 0), label="Pending", color="#2b5c8f", edgecolor="black")

    ax.set_title("Monthly Case Filings by Final Status", fontsize=12, fontweight="bold")
    ax.set_xlabel("Filing Month")
    ax.set_ylabel("Cases Filed")
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend(title="Status", frameon=True)

    plt.tight_layout()
    fig3_path = fig_dir / "fig3_filing_trends.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()

    # 4. Figure 4: Kaplan-Meier Non-parametric Survival Curve
    t_vals = np.sort(df["duration_days"].unique())
    surv_prob = 1.0
    current_risk = len(df)
    timeline = [0]
    probabilities = [1.0]

    for time_point in t_vals:
        at_this_time = df[df["duration_days"] == time_point]
        d_i = (at_this_time["case_status"] == "Disposed").sum()
        c_i = (at_this_time["case_status"] == "Pending").sum()

        if current_risk > 0:
            surv_prob *= (1.0 - (d_i / current_risk))
            timeline.append(time_point)
            probabilities.append(surv_prob)
            current_risk -= (d_i + c_i)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.step(timeline, probabilities, where="post", color="#1b7837", linewidth=2.5, label="Survival Probability (P(Pendency > t))")
    ax.axhline(0.5, color="gray", linestyle="--", alpha=0.7, label="50% Probability Line")
    ax.set_title("Kaplan-Meier Pendency Survival Curve (Kollam NI-138 Cases)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Time from Filing (Days)")
    ax.set_ylabel("Estimated Probability of Remaining Pending")
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(frameon=True)

    plt.tight_layout()
    fig4_path = fig_dir / "fig4_kaplan_meier_survival.png"
    plt.savefig(fig4_path, dpi=300)
    plt.close()

    # Descriptive metrics
    stats = {
        "total_cases": int(len(df)),
        "disposed_cases": int(len(disposed)),
        "pending_cases": int(len(df) - len(disposed)),
        "disposal_rate": float(len(disposed) / len(df)),
        "disposed_duration_mean": float(disposed["duration_days"].mean()),
        "disposed_duration_std": float(disposed["duration_days"].std()),
        "disposed_duration_median": float(disposed["duration_days"].median()),
        "disposed_duration_iqr": float(disposed["duration_days"].quantile(0.75) - disposed["duration_days"].quantile(0.25)),
        "disposed_duration_min": int(disposed["duration_days"].min()),
        "disposed_duration_max": int(disposed["duration_days"].max()),
        "skewness": float(disposed["duration_days"].skew()),
        "kurtosis": float(disposed["duration_days"].kurtosis()),
    }

    with open(output_stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print("EDA Visualizations and metrics generated successfully.")
    return stats


if __name__ == "__main__":
    run_eda()
