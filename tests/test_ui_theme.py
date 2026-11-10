"""
JusticeLink AI: UI Component and Theme tests.
"""

from justicelink.ui.theme import THEME_CSS
from justicelink.ui.components import render_header, render_card, render_footer


def test_theme_css_structure():
    assert "#FDFBF7" in THEME_CSS
    assert "#6B1D2F" in THEME_CSS
    assert "national-emblem-ribbon" in THEME_CSS
    assert "judicial-card" in THEME_CSS
