"""
JusticeLink AI: Main Application Entry Point with Institutional Navigation.
Coordinates all 6 modular pages while strictly preserving existing ML models and APIs.
"""

from __future__ import annotations

import streamlit as st
from justicelink.ui.theme import apply_theme
from justicelink.ui.components import render_header, render_footer

# Configure page metadata
st.set_page_config(
    page_title="JusticeLink AI · Judicial Case Analytics",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Institutional Indian Judicial Styling
apply_theme()

# Top Header Ribbon
render_header()

# Sidebar Navigation with State Management
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0 16px 0; border-bottom: 2px solid #C29B38; margin-bottom: 15px;">
        <span style="font-size: 2.2rem;">🏛️</span>
        <h3 style="margin: 4px 0 0 0; color: #6B1D2F; font-size: 1.15rem;">JUSTICELINK AI</h3>
        <p style="margin: 0; font-size: 0.75rem; color: #5A6270; letter-spacing: 0.5px;">JUDICIAL INTELLIGENCE SYSTEM</p>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES = [
    "🏛️ 1. Platform Overview & Hero",
    "🗺️ 2. India Judicial Map Explorer",
    "📊 3. Judicial Backlog & Survival Analytics",
    "🔬 4. ML Research Lab & Benchmarks",
    "⚖️ 5. Explainable Case Prioritization",
    "📑 6. Research Methodology & Data Spec",
]

if "current_page" not in st.session_state:
    st.session_state.current_page = PAGES[0]

selected_page = st.sidebar.radio(
    "PORTAL NAVIGATION",
    PAGES,
    index=PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0,
)
st.session_state.current_page = selected_page

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="background-color: #EDE4D1; padding: 12px; border-radius: 6px; border-left: 3px solid #6B1D2F;">
        <p style="margin: 0; font-size: 0.75rem; color: #3A404D; line-height: 1.4;">
            <strong>Jurisdiction Scope:</strong><br>
            Kerala District Courts (14 Districts, 180 Complexes)<br>
            <strong>Research Corpus:</strong><br>
            Kollam NI-138 Lifecycle Pilot
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Route to respective modular page implementation
if selected_page == "🏛️ 1. Platform Overview & Hero":
    from justicelink.ui.pages import p01_landing
    p01_landing.render()

elif selected_page == "🗺️ 2. India Judicial Map Explorer":
    from justicelink.ui.pages import p02_map
    p02_map.render()

elif selected_page == "📊 3. Judicial Backlog & Survival Analytics":
    from justicelink.ui.pages import p03_analytics
    p03_analytics.render()

elif selected_page == "🔬 4. ML Research Lab & Benchmarks":
    from justicelink.ui.pages import p04_ml_lab
    p04_ml_lab.render()

elif selected_page == "⚖️ 5. Explainable Case Prioritization":
    from justicelink.ui.pages import p05_ranking
    p05_ranking.render()

elif selected_page == "📑 6. Research Methodology & Data Spec":
    from justicelink.ui.pages import p06_research
    p06_research.render()

# Global Institutional Footer
render_footer()
