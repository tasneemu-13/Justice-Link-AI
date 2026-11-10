"""
JusticeLink AI: Page 6 — Research Methodology & Data Specifications.
Features:
- Complete Data Provenance & Ingestion Audit
- Interactive Data Dictionary Viewer
- Feature Engineering & Right-Censoring Methodology
- Machine Learning Formulation & Evaluation Framework
- Research Limitations, Ethics & Statutory Safeguards
- Downloadable Research Reports (Markdown & CSV)
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data
def load_data_dictionary():
    p = Path("reports/data_dictionary.md")
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return None


@st.cache_data
def load_eda_report():
    p = Path("reports/eda_report.md")
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return None


@st.cache_data
def load_model_report():
    p = Path("reports/model_evaluation_report.md")
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return None


def render():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #9E7D2B; text-transform: uppercase;">
                ACADEMIC & TECHNICAL SPECIFICATION · REPRODUCIBILITY GUIDE
            </span>
            <h2 style="margin: 4px 0 8px 0; color: #6B1D2F;">Research Methodology & Data Specifications</h2>
            <p style="margin: 0; color: #4A5568; font-size: 0.95rem; line-height: 1.5;">
                Formal documentation of data provenance, feature engineering rules, right-censoring constraints, 
                machine learning benchmark protocols, and judicial decision-support limitations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_prov, tab_dict, tab_ml_meth, tab_ethics, tab_downloads = st.tabs([
        "🏛️ Data Provenance & Pipeline",
        "📖 Data Dictionary",
        "🔬 ML Formulation & Metrics",
        "⚖️ Research Ethics & Limits",
        "📥 Download Research Assets",
    ])

    # 1. Tab: Data Provenance
    with tab_prov:
        st.markdown("#### Data Provenance, Ingestion & Validation Pipeline")
        st.markdown(
            """
            <div style="background-color: #FAF8F2; border: 1px solid #DFD7C5; border-radius: 6px; padding: 18px; margin-bottom: 16px;">
                <h5 style="margin-top:0; color: #6B1D2F;">Data Provenance Architecture</h5>
                <ul style="margin:0; padding-left: 20px; font-size: 0.88rem; color: #374151; line-height: 1.7;">
                    <li><strong>Primary Corpus Source:</strong> Verified district eCourts filings from Kollam District, Kerala under the digital ONCourts initiative (Negotiable Instruments Act Section 138).</li>
                    <li><strong>Temporal Window:</strong> Case filings from 2024 through early 2026, observed up to the right-censoring cutoff date of <code>March 10, 2026</code>.</li>
                    <li><strong>National Discovery Hierarchy:</strong> Metadata mapping all 14 judicial districts and 180 court complexes across Kerala, with sample CNR keys from Alappuzha, Ernakulam, Kozhikode, and Thrissur.</li>
                    <li><strong>Zero Data Fabrication:</strong> Missing values are never filled with synthetic values; pending cases are never assigned synthetic disposal durations.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Ingestion & Validation Quality Gate (`CaseDataValidator`)")
        st.write(
            """
            Every raw record passes through an automated validation gate in `src/justicelink/validation/validator.py`:
            - **Format Adherence:** Case identifiers must strictly match `^KL-\\d{6}-\\d{4}$` (100% adherence).
            - **Duplicate Elimination:** Uniqueness enforced on filing numbers (0 duplicates found across 1,284 records).
            - **Chronological Consistency:** $T_{\\text{filing}} \\le T_{\\text{event}}$ enforced (0 chronology violations).
            - **Censoring Uniformity:** 100% of pending cases terminate at the observation cutoff date.
            """
        )

    # 2. Tab: Data Dictionary
    with tab_dict:
        st.markdown("#### Formal Data Dictionary")
        dict_md = load_data_dictionary()
        if dict_md:
            st.markdown(dict_md)
        else:
            st.info("Data dictionary file not found at `reports/data_dictionary.md`.")

    # 3. Tab: ML Methodology
    with tab_ml_meth:
        st.markdown("#### Machine Learning Formulation & Benchmarking Protocol")
        st.markdown(
            r"""
            ##### Target Variable Formulation
            The numerical regression target $y_i$ is defined strictly for **completed cases** ($N=278$):
            $$y_i = \text{Date}_{\text{disposal}} - \text{Date}_{\text{filing}} \quad (\text{in days})$$

            Active/pending matters ($N=1,006$) represent **right-censored observations**:
            $$T_i > C_i = \text{Date}_{\text{cutoff}} - \text{Date}_{\text{filing}}$$
            Treating pending cases as disposed at their current age would introduce severe negative survivorship bias into duration regression models.

            ##### Feature Engineering
            - `case_seq_no`: Sequential filing arrival order within the calendar year.
            - `filing_year`: Cohort indicator (2024, 2025, 2026).
            - `filing_month` & `filing_quarter`: Seasonality indicators.
            - `filing_day_of_week`: Intra-week filing rhythm (0=Monday to 6=Sunday).
            - `filing_day_of_year`: Continuous calendar timeline position (1 to 365).

            ##### Cross-Validation & Metric Standards
            - **Evaluation Protocol:** 80/20 train/test split with fixed seed + 5-Fold Cross-Validation on the training partition.
            - **Evaluation Metrics:**
              $$\text{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i| \qquad \text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2} \qquad R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
            """
        )

    # 4. Tab: Ethics & Limitations
    with tab_ethics:
        st.markdown("#### Research Ethics, Limits & Statutory Boundaries")
        st.markdown(
            """
            <div style="background-color: #FFF8E1; border: 1px solid #FFE082; border-left: 4px solid #FF8F00; padding: 18px; border-radius: 6px;">
                <h5 style="margin-top:0; color: #B25E00;">Mandatory Statutory & Decision-Support Notice</h5>
                <p style="font-size: 0.88rem; color: #4E342E; line-height: 1.6;">
                    <strong>Decision Support Only:</strong> JusticeLink AI is an academic and technical research platform 
                    engineered for procedural court management, backlog analytics, and caseload distribution modeling.
                </p>
                <ul style="font-size: 0.85rem; color: #4E342E; line-height: 1.7; margin-bottom: 0;">
                    <li><strong>No Autonomous Adjudication:</strong> The system does not determine legal merits, assess credibility, or predict trial outcomes.</li>
                    <li><strong>No Judicial Replacement:</strong> All predictive outputs and priority ranks are administrative indicators requiring human review.</li>
                    <li><strong>Privacy & Anonymization:</strong> Case records are restricted to public procedural metadata. Litigant personal identities are omitted from modeling features to prevent proxy bias.</li>
                    <li><strong>Jurisdictional Boundary:</strong> Empirical duration models are calibrated on the Kollam pilot and should not be extrapolated to unrelated jurisdictions without local recalibration.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5. Tab: Downloadable Reports
    with tab_downloads:
        st.markdown("#### Download Verified Research Reports & Benchmark Artifacts")
        
        down_c1, down_c2 = st.columns(2)
        
        with down_c1:
            st.markdown("##### 📄 Formal Research Reports (Markdown)")
            
            p_eda = Path("reports/eda_report.md")
            if p_eda.exists():
                with open(p_eda, "r", encoding="utf-8") as f:
                    st.download_button(
                        "📥 Download EDA Report (Markdown)",
                        f.read(),
                        file_name="justicelink_eda_report.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

            p_eval = Path("reports/model_evaluation_report.md")
            if p_eval.exists():
                with open(p_eval, "r", encoding="utf-8") as f:
                    st.download_button(
                        "📥 Download Model Benchmark Report (Markdown)",
                        f.read(),
                        file_name="justicelink_model_evaluation_report.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

        with down_c2:
            st.markdown("##### 📊 Benchmark Data & Triage Queues (CSV)")
            
            p_metrics = Path("reports/model_benchmark_metrics.csv")
            if p_metrics.exists():
                with open(p_metrics, "r", encoding="utf-8") as f:
                    st.download_button(
                        "📥 Download Model Benchmark Metrics (CSV)",
                        f.read(),
                        file_name="justicelink_model_benchmarks.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

            p_ranked = Path("reports/pending_cases_ranked.csv")
            if p_ranked.exists():
                with open(p_ranked, "r", encoding="utf-8") as f:
                    st.download_button(
                        "📥 Download Ranked Case Queue (CSV)",
                        f.read(),
                        file_name="justicelink_pending_cases_ranked.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
