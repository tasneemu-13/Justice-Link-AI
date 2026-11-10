"""
JusticeLink AI: Institutional Design System & Custom CSS.
Colors:
- Background: Warm ivory (#FDFBF7) and antique cream (#F7F4EB)
- Containers/Cards: Warm beige (#EFE9DC), light sand (#E6DEC8)
- Institutional Primary: Indian judicial maroon / deep burgundy (#6B1D2F, #80182A)
- Accents: Burnished gold (#9E7D2B), muted sandstone (#C29B38)
- Typography: Charcoal (#1E232A), Muted slate (#4A5568)
"""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Main Canvas Styling */
.stApp {
    background-color: #FDFBF7 !important;
    color: #1E232A !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background-color: #F6F2E8 !important;
    border-right: 1px solid #DFD7C5 !important;
}

section[data-testid="stSidebar"] div.stRadio > label {
    font-weight: 700 !important;
    color: #6B1D2F !important;
    font-size: 0.95rem !important;
}

/* Radio buttons in sidebar */
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background-color: transparent !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    margin-bottom: 4px !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    background-color: #EDE4D1 !important;
}

/* Institutional Headings */
h1, h2, h3 {
    color: #6B1D2F !important;
    font-family: 'Cinzel', serif, Georgia !important;
    letter-spacing: 0.5px !important;
    font-weight: 700 !important;
}

h4, h5, h6 {
    color: #2D3748 !important;
    font-weight: 600 !important;
}

/* Institutional Top Header Ribbon */
.national-emblem-ribbon {
    background: linear-gradient(90deg, #6B1D2F 0%, #80182A 50%, #6B1D2F 100%);
    color: #FDFBF7;
    padding: 10px 24px;
    border-radius: 6px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 3px solid #C29B38;
    box-shadow: 0 4px 12px rgba(107, 29, 47, 0.12);
}

.national-emblem-ribbon h1 {
    color: #FFFFFF !important;
    margin: 0 !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}

.national-emblem-ribbon p {
    color: #F3EFE6 !important;
    margin: 0 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px !important;
}

/* Card Containers */
.judicial-card {
    background-color: #FFFFFF;
    border: 1px solid #DFD7C5;
    border-top: 3px solid #6B1D2F;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(30, 35, 42, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.judicial-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(107, 29, 47, 0.08);
}

.judicial-card-gold {
    background-color: #FAF7EE;
    border: 1px solid #D6C8A8;
    border-top: 3px solid #9E7D2B;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(158, 125, 43, 0.06);
}

/* Metrics Display */
div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DFD7C5 !important;
    border-radius: 8px !important;
    padding: 14px 18px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
    border-left: 4px solid #6B1D2F !important;
}

div[data-testid="stMetric"] label {
    color: #5A6270 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #6B1D2F !important;
    font-weight: 800 !important;
    font-size: 1.8rem !important;
}

/* Buttons */
.stButton > button {
    background-color: #6B1D2F !important;
    color: #FFFFFF !important;
    border: 1px solid #541423 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #80182A !important;
    border-color: #9E7D2B !important;
    color: #FDFBF7 !important;
    box-shadow: 0 4px 10px rgba(107, 29, 47, 0.2) !important;
}

/* Secondary Button styling */
.btn-gold {
    background-color: #9E7D2B !important;
    color: #FFFFFF !important;
}

/* Dataframe & Tables */
div[data-testid="stDataFrame"] {
    border: 1px solid #DFD7C5 !important;
    border-radius: 6px !important;
    background-color: #FFFFFF !important;
}

/* Custom Badges */
.badge-disposed {
    background-color: #E8F5E9;
    color: #1E6B2A;
    border: 1px solid #A5D6A7;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.78rem;
    font-weight: 700;
}

.badge-pending {
    background-color: #FFF3E0;
    color: #B25E00;
    border: 1px solid #FFE0B2;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.78rem;
    font-weight: 700;
}

.badge-priority {
    background-color: #FFEBEE;
    color: #A31224;
    border: 1px solid #FFCDD2;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.78rem;
    font-weight: 700;
}

/* Institutional Disclaimer Footer */
.institutional-footer {
    border-top: 1px solid #DFD7C5;
    padding: 24px 10px 10px 10px;
    margin-top: 40px;
    color: #6B7280;
    font-size: 0.8rem;
    text-align: center;
}

.institutional-footer a {
    color: #6B1D2F;
    text-decoration: none;
    font-weight: 600;
}
</style>
"""


def apply_theme():
    """Injects custom Indian judicial institutional CSS."""
    import streamlit as st
    st.markdown(THEME_CSS, unsafe_allow_html=True)
