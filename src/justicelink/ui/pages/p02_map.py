"""
JusticeLink AI: Page 2 — Interactive India Judicial Map Explorer.
Features:
- State-by-State Judicial Presence Map across India
- Jurisdictional metadata distinction (Discovery Tree vs Training Case Records)
- Deep-dive into Kerala (all 14 districts & 180 court complexes)
- CNR Key Inspector (1,239 verified multi-district CNR identifiers)
- Configurable research scope (Kerala/Kollam active pilot vs upcoming state nodes)
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def load_kerala_metadata():
    p = Path("data/raw/kerala/kerala_district_courts_metadata.json")
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        tree = json.load(f)

    districts = tree.get("Kerala", {}).get("districts", {})
    records = []
    for d_name, d_info in districts.items():
        dstvalue = d_info.get("dstvalue", "")
        complexes = d_info.get("court_complexes", {})
        for c_name, c_info in complexes.items():
            records.append({
                "State": "Kerala",
                "District": d_name,
                "District_Code": dstvalue,
                "Court_Complex": c_name,
                "Court_Value": c_info.get("crtvalue", ""),
            })
    return pd.DataFrame(records)


@st.cache_data
def load_sample_keys():
    p = Path("data/raw/kerala/kerala_sample_case_keys.txt")
    if not p.exists():
        return None
    records = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|")
                if len(parts) == 4:
                    records.append({
                        "District": parts[0],
                        "Court_Complex": parts[1],
                        "Case_Query_ID": parts[2],
                        "CNR_Number": parts[3],
                    })
    return pd.DataFrame(records)


def render():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #9E7D2B; text-transform: uppercase;">
                GEOGRAPHIC RECONNAISSANCE · NATIONAL EC OURTS DISCOVERY
            </span>
            <h2 style="margin: 4px 0 8px 0; color: #6B1D2F;">Interactive India Judicial Map & Metadata Explorer</h2>
            <p style="margin: 0; color: #4A5568; font-size: 0.95rem; line-height: 1.5;">
                Explore state-level judicial data readiness across the Republic of India. 
                Distinguishes between <strong>Administrative Discovery Trees</strong> (court complexes, establishment hierarchy) 
                and <strong>Active ML-Trained Case Corpora</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. State Coverage Data
    states_data = pd.DataFrame([
        {"State": "Kerala", "Status": "Active Pilot (Trained Corpus)", "Complexes": 180, "Districts": 14, "Cases_Available": 1284, "Latitude": 10.8505, "Longitude": 76.2711, "Color": "#6B1D2F"},
        {"State": "Madhya Pradesh", "Status": "Configured Discovery Node", "Complexes": 52, "Districts": 55, "Cases_Available": 0, "Latitude": 22.9734, "Longitude": 78.6569, "Color": "#C29B38"},
        {"State": "Haryana", "Status": "Configured Discovery Node", "Complexes": 22, "Districts": 22, "Cases_Available": 0, "Latitude": 29.0588, "Longitude": 76.0856, "Color": "#C29B38"},
        {"State": "Punjab", "Status": "Configured Discovery Node", "Complexes": 23, "Districts": 23, "Cases_Available": 0, "Latitude": 31.1471, "Longitude": 75.3412, "Color": "#C29B38"},
        {"State": "Gujarat", "Status": "Sampled Discovery Node", "Complexes": 33, "Districts": 33, "Cases_Available": 0, "Latitude": 22.2587, "Longitude": 71.1924, "Color": "#C29B38"},
        {"State": "Maharashtra", "Status": "Planned Discovery Node", "Complexes": 36, "Districts": 36, "Cases_Available": 0, "Latitude": 19.7515, "Longitude": 75.7139, "Color": "#A0AEC0"},
        {"State": "Tamil Nadu", "Status": "Planned Discovery Node", "Complexes": 38, "Districts": 38, "Cases_Available": 0, "Latitude": 11.1271, "Longitude": 78.6569, "Color": "#A0AEC0"},
        {"State": "Karnataka", "Status": "Planned Discovery Node", "Complexes": 31, "Districts": 31, "Cases_Available": 0, "Latitude": 15.3173, "Longitude": 75.7139, "Color": "#A0AEC0"},
        {"State": "Uttar Pradesh", "Status": "Planned Discovery Node", "Complexes": 75, "Districts": 75, "Cases_Available": 0, "Latitude": 26.8467, "Longitude": 80.9462, "Color": "#A0AEC0"},
    ])

    col_map, col_state_details = st.columns([13, 11])

    with col_map:
        st.markdown("#### 🗺️ National Judicial Node Geographic Distribution")
        
        fig = go.Figure()

        # Add Scatter geo points
        fig.add_trace(go.Scattergeo(
            lon=states_data["Longitude"],
            lat=states_data["Latitude"],
            text=states_data.apply(
                lambda r: f"<b>{r['State']}</b><br>Status: {r['Status']}<br>Complexes: {r['Complexes']}<br>Cases: {r['Cases_Available']}",
                axis=1
            ),
            mode="markers+text",
            textposition="top center",
            textfont=dict(family="Plus Jakarta Sans", size=10, color="#1E232A"),
            marker=dict(
                size=[26 if s == "Kerala" else 14 for s in states_data["State"]],
                color=states_data["Color"],
                opacity=0.9,
                line=dict(width=1.5, color="#FFFFFF"),
            ),
            hoverinfo="text",
        ))

        fig.update_layout(
            geo=dict(
                scope="asia",
                center=dict(lat=22.0, lon=78.5),
                projection_scale=3.8,
                showland=True,
                landcolor="#F7F3E9",
                showcountries=True,
                countrycolor="#DDD4C4",
                showsubunits=True,
                subunitcolor="#E8E1D3",
                bgcolor="#FDFBF7",
            ),
            margin=dict(l=0, r=0, t=10, b=10),
            height=430,
            paper_bgcolor="#FDFBF7",
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_state_details:
        st.markdown("#### 🏛️ State Jurisdictional Profile Inspector")
        selected_state = st.selectbox("Select State to Inspect:", states_data["State"].tolist(), index=0)

        state_row = states_data[states_data["State"] == selected_state].iloc[0]

        is_active = (selected_state == "Kerala")
        card_bg = "#FFFFFF" if is_active else "#FAF8F2"
        border_col = "#6B1D2F" if is_active else "#C29B38"

        st.markdown(
            f"""
            <div style="background-color: {card_bg}; border: 1px solid #DFD7C5; border-left: 4px solid {border_col}; padding: 16px 20px; border-radius: 6px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color: #6B1D2F; font-size: 1.3rem;">{selected_state}</h3>
                    <span style="font-size:0.75rem; font-weight:700; background:{'#E8F5E9' if is_active else '#FFF3E0'}; color:{'#1E6B2A' if is_active else '#B25E00'}; padding:4px 8px; border-radius:4px;">
                        {state_row['Status']}
                    </span>
                </div>
                <div style="margin-top: 14px; font-size: 0.88rem; color: #4A5568; line-height: 1.6;">
                    <p style="margin:4px 0;"><strong>Judicial Districts:</strong> {state_row['Districts']}</p>
                    <p style="margin:4px 0;"><strong>Cataloged Court Complexes:</strong> {state_row['Complexes']}</p>
                    <p style="margin:4px 0;"><strong>Active Case-Level Records:</strong> {state_row['Cases_Available']}</p>
                    <p style="margin:4px 0;"><strong>Repository Provenance:</strong> {'Live eCourts Scraper & Kollam ONCourts Corpus' if is_active else 'State Discovery Schema Available'}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not is_active:
            st.info(
                f"ℹ️ **Research Integrity Note:** {selected_state} currently has administrative court tree metadata "
                f"cataloged in configs. Case-level empirical models are trained on the active Kerala corpus to avoid fabricated data."
            )

    st.markdown("---")

    # 2. Kerala Deep-Dive (Districts and Court Complexes)
    st.markdown("### 🌴 Kerala Deep Dive: 14 Judicial Districts & 180 Court Complexes")
    df_kerala = load_kerala_metadata()

    if df_kerala is not None:
        c_tree, c_dist_chart = st.columns([14, 10])

        with c_dist_chart:
            st.markdown("#### Court Complexes per District")
            dist_counts = df_kerala.groupby("District")["Court_Complex"].count().reset_index()
            dist_counts.columns = ["District", "Complex_Count"]
            dist_counts = dist_counts.sort_values("Complex_Count", ascending=True)

            bar_fig = px.bar(
                dist_counts,
                x="Complex_Count",
                y="District",
                orientation="h",
                color="Complex_Count",
                color_continuous_scale=["#C29B38", "#6B1D2F"],
                text="Complex_Count",
            )
            bar_fig.update_layout(
                xaxis_title="Cataloged Court Complexes",
                yaxis_title="",
                height=420,
                paper_bgcolor="#FDFBF7",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=10, r=20, t=10, b=10),
                coloraxis_showscale=False,
            )
            bar_fig.update_traces(textposition="outside")
            st.plotly_chart(bar_fig, use_container_width=True)

        with c_tree:
            st.markdown("#### District Court Complex Directory")
            filter_district = st.selectbox(
                "Filter by Judicial District:",
                ["All 14 Districts"] + sorted(df_kerala["District"].unique().tolist()),
                index=0,
            )

            view_df = df_kerala if filter_district == "All 14 Districts" else df_kerala[df_kerala["District"] == filter_district]

            st.dataframe(
                view_df[["District", "Court_Complex", "Court_Value"]],
                use_container_width=True,
                height=380,
            )

    st.markdown("---")

    # 3. Verified Sample CNR Keys Across Kerala
    st.markdown("### 🔑 Verified Case Identifiers: Multi-District Sample (1,239 CNR Keys)")
    df_keys = load_sample_keys()

    if df_keys is not None:
        k_col1, k_col2 = st.columns([1, 2])
        with k_col1:
            st.markdown("#### Sample Keys by District")
            key_summary = df_keys["District"].value_counts().reset_index()
            key_summary.columns = ["District", "Verified_Keys"]
            st.dataframe(key_summary, use_container_width=True, height=340)

        with k_col2:
            st.markdown("#### CNR Key Lookup Table")
            search_cnr = st.text_input("Search by CNR or District (e.g. KLAL or Kollam):", "")
            filtered_keys = df_keys
            if search_cnr:
                filtered_keys = df_keys[
                    df_keys["District"].str.contains(search_cnr, case=False) |
                    df_keys["CNR_Number"].str.contains(search_cnr, case=False) |
                    df_keys["Court_Complex"].str.contains(search_cnr, case=False)
                ]
            st.dataframe(filtered_keys, use_container_width=True, height=340)
