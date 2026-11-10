"""
JusticeLink AI: Reusable Institutional UI Components.
Includes:
- Judicial Header Ribbon
- Institutional Metric Cards
- Badges and Status Pills
- Institutional Disclaimer & Breadcrumb Bar
- Court Metadata Pill Box
"""

from __future__ import annotations

import streamlit as st


def render_header():
    """Renders the top national judicial branding ribbon."""
    st.markdown(
        """
        <div class="national-emblem-ribbon">
            <div>
                <h1>JUSTICELINK AI · न्याय सेतु</h1>
                <p>EXPLAINABLE MACHINE LEARNING JUDICIAL ANALYTICS & CASE RANKING PLATFORM</p>
            </div>
            <div style="text-align: right; display: flex; align-items: center; gap: 12px;">
                <span style="background: rgba(255,255,255,0.15); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #C29B38; color: #FFF;">
                    PILOT: KERALA DISTRICT COURTS
                </span>
                <span style="font-size: 1.4rem;">⚖️</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, content_html: str, gold_border: bool = False):
    """Renders a styled judicial institutional card."""
    css_class = "judicial-card-gold" if gold_border else "judicial-card"
    st.markdown(
        f"""
        <div class="{css_class}">
            <h4 style="margin-top:0; color: #6B1D2F; border-bottom: 1px solid #DFD7C5; padding-bottom: 8px;">{title}</h4>
            <div>{content_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    """Renders the institutional research disclaimer and provenance footer."""
    st.markdown(
        """
        <div class="institutional-footer">
            <p><strong>JusticeLink AI</strong> · Research-Grade Explainable Judicial Analytics & Decision Support System</p>
            <p>
                <strong>Statutory Notice:</strong> This platform is designed exclusively for case-management diagnostics, 
                court backlog analytics, and procedural review prioritization. It does not provide legal counsel, 
                predict case merits, or substitute for the sovereign discretion of the judiciary.
            </p>
            <p style="margin-top: 8px;">
                Reference Standard: eCourts Services & Kollam ONCourts Initiative · Built with Python & Streamlit
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
