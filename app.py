
from pathlib import Path
from datetime import date
import uuid

import pandas as pd
import pydeck as pdk
import streamlit as st

# --------------------------------------------------
# CivicAI | Civic Issue Intelligence
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "complaints.csv"
LOGO_PATH = BASE_DIR / "civicai_logo.png"

DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="CivicAI | Civic Issue Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Calm navy + blue + teal + green theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #101b36;
        --blue: #477fe5;
        --teal: #36b7b0;
        --green: #35ad70;
        --text: #eaf0ff;
        --muted: #aab8d3;
        --panel: rgba(25, 39, 70, 0.78);
        --border: rgba(150, 177, 224, 0.19);
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 12%, rgba(58, 101, 190, 0.20), transparent 38%),
            radial-gradient(ellipse at 86% 22%, rgba(38, 159, 151, 0.12), transparent 35%),
            linear-gradient(135deg, #0c1530 0%, #111d3b 48%, #101a32 100%);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }

    /* Subtle moving light: no images, no JavaScript */
    .stApp::before {
        content: "";
        position: fixed;
        inset: -40%;
        z-index: 0;
        pointer-events: none;
        background: conic-gradient(
            from 0deg at 50% 50%,
            transparent 0deg,
            rgba(60, 126, 219, 0.07) 65deg,
            transparent 130deg,
            rgba(43, 183, 165, 0.06) 210deg,
            transparent 280deg
        );
        animation: slowGlow 32s linear infinite;
    }

    @keyframes slowGlow {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    [data-testid="stHeader"] {
        background: rgba(12, 21, 48, 0.72);
    }

    [data-testid="stSidebar"] {
        background: rgba(12, 22, 45, 0.94);
        border-right: 1px solid var(--border);
    }

    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: #f4f7ff !important;
        letter-spacing: -0.5px;
    }

    p, label, span, div {
        font-family: 'DM Sans', sans-serif;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 26px 30px;
        border: 1px solid var(--border);
        border-radius: 22px;
        background: linear-gradient(
            115deg,
            rgba(38, 61, 108, 0.86),
            rgba(22, 43, 73, 0.80) 58%,
            rgba(25, 83, 88, 0.45)
        );
        margin-bottom: 24px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.12);
        animation: enterUp 0.7s ease both;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -80px;
        top: -110px;
        border-radius: 50%;
        border: 1px solid rgba(110, 180, 238, 0.22);
        box-shadow: 0 0 0 28px rgba(100, 160, 225, 0.035),
                    0 0 0 58px rgba(100, 160, 225, 0.025);
        animation: breathe 7s ease-in-out infinite;
    }

    @keyframes breathe {
        0%, 100% { transform: scale(1); opacity: 0.65; }
        50% { transform: scale(1.08); opacity: 1; }
    }

    @keyframes enterUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .eyebrow {
        color: #77d8cf;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.15;
        font-weight: 800;
        margin: 0;
        color: #f6f8ff;
    }

    .hero-title .accent { color: #62d3aa; }

    .hero-subtitle {
        color: #c0cde5;
        font-size: 1rem;
        margin-top: 12px;
        max-width: 720px;
        line-height: 1.7;
    }

    .section-kicker {
        color: #85d7d0;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .metric-card {
        background: linear-gradient(145deg, rgba(34, 51, 87, 0.88),
                                    rgba(23, 38, 67, 0.83));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 122px;
        transition: transform 0.25s ease, border-color 0.25s ease;
        animation: enterUp 0.6s ease both;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(91, 190, 190, 0.48);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.86rem;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #f5f7ff;
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Manrope', sans-serif;
    }

    .metric-note {
        color: #83d7bc;
        font-size: 0.78rem;
        margin-top: 4px;
    }

    .info-panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .small-muted {
        color: var(--muted);
        font-size: 0.88rem;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        border: 1px solid rgba(104, 180, 211, 0.35);
        background: linear-gradient(100deg, #356ed0, #238e91);
        color: white;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        border-color: #7edfd0;
        transform: translateY(-1px);
        color: white;
    }

    [data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--border);
        padding: 16px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: #f5f7ff; }

    [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--border);
    }

    [data-baseweb="tab"] {
        background: rgba(29, 45, 77, 0.6);
        border-radius: 10px 10px 0 0;
        padding: 12px 18px;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(54, 123, 157, 0.30);
    }

    input, textarea {
        background-color: rgba(15, 28, 53, 0.75) !important;
    }

    hr { border-color: var(--border); }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Demo data: created automatically if CSV is missing
# --------------------------------------------------

COLUMNS = [
    "id", "text", "category", "urgency",
    "lat", "lon", "date", "issue_id", "status"
]

SAMPLE_ROWS = [
    ["C001", "Large pothole near the main market", "Roads", 5, 22.7196, 75.8577, "2026-10-20", "ISS-001", "Open"],
    ["C002", "Road damaged near the bus stop", "Roads", 4, 22.7210, 75.8610, "2026-10-21", "ISS-001", "Open"],
    ["C003", "Pothole causing traffic problems", "Roads", 5, 22.7185, 75.8550, "2026-10-22", "ISS-001", "Open"],
    ["C004", "Water supply has been interrupted", "Water", 4, 22.7250, 75.8500, "2026-10-20", "ISS-002", "Open"],
    ["C005", "No water supply since yesterday", "Water", 5, 22.7260, 75.8510, "2026-10-21", "ISS-002", "Open"],
    ["C006", "Garbage has not been collected", "Sanitation", 3, 22.7150, 75.8650, "2026-10-20", "ISS-003", "Open"],
    ["C007", "Overflowing garbage bin near the park", "Sanitation", 4, 22.7160, 75.8660, "2026-10-22", "ISS-003", "Open"],
    ["C008", "Streetlight not working on this road", "Streetlights", 3, 22.7300, 75.8700, "2026-10-20", "ISS-004", "Open"],
    ["C009", "The street is very dark at night", "Streetlights", 4, 22.7310, 75.8690, "2026-10-22", "ISS-004", "Open"],
    ["C010", "Broken road surface near school", "Roads", 4, 22.7220, 75.8580, "2026-10-23", "ISS-001", "Open"],
    ["C011", "Dirty water coming from the tap", "Water", 5, 22.7270, 75.8520, "2026-10-23", "ISS-005", "Open"],
    ["C012", "Waste scattered beside the road", "Sanitation", 3, 22.7140, 75.8640, "2026-10-23", "ISS-003", "Open"],
    ["C013", "Streetlight flickers and switches off", "Streetlights", 3, 22.7320, 75.8710, "2026-10-23", "ISS-004", "Open"],
    ["C014", "Deep pothole creating accident risk", "Roads", 5, 22.7205, 75.8560, "2026-10-24", "ISS-001", "Open"],
    ["C015", "Low water pressure in the neighbourhood", "Water", 3, 22.7280, 75.8530, "2026-10-24", "ISS-002", "Open"],
]


def ensure_csv():
    if not CSV_PATH.exists():
        pd.DataFrame(SAMPLE_ROWS, columns=COLUMNS).to_csv(CSV_PATH, index=False)


def load_data():
    ensure_csv()
    df = pd.read_csv(CSV_PATH)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    df["urgency"] = pd.to_numeric(df["urgency"], errors="coerce").fillna(3)
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["category"] = df["category"].fillna("Other")
    df["status"] = df["status"].fillna("Open")
    df["text"] = df["text"].fillna("")
    df["issue_id"] = df["issue_id"].fillna("ISS-NEW")
    return df


def save_data(df):
    df.to_csv(CSV_PATH, index=False)


def priority_score(group):
    # Demo ranking only; weights are provisional and not validated.
    volume = min(len(group) / 5, 1) * 35
    severity = (group["urgency"].mean() / 5) * 30
    duration = 10  # Placeholder until issue duration is calculated reliably.
    concentration = min(len(group) / 8, 1) * 15
    return round(volume + severity + duration + concentration, 1)


def make_issue_table(df):
    if df.empty:
        return pd.DataFrame()

    rows = []
    for issue_id, group in df.groupby("issue_id"):
        rows.append({
            "Issue ID": issue_id,
            "Category": group["category"].mode().iloc[0],
            "Complaints": len(group),
            "Avg. urgency": round(group["urgency"].mean(), 1),
            "Priority score": priority_score(group),
            "Status": group["status"].mode().iloc[0],
            "Example complaint": group["text"].iloc[0],
        })

    return pd.DataFrame(rows).sort_values(
        "Priority score", ascending=False
    ).reset_index(drop=True)


df = load_data()
issues = make_issue_table(df)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.markdown("## <span style='color:#64d7b0'>Civic</span>AI", unsafe_allow_html=True)

    st.caption("CIVIC ISSUE INTELLIGENCE")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Report a complaint",
            "Issue intelligence",
            "Issue map",
            "Officer action",
        ],
    )

    st.divider()
    st.markdown("**Prototype status**")
    st.markdown(
        "<span style='color:#7ed9bd'>●</span> Demo mode",
        unsafe_allow_html=True,
    )
    st.caption("Sample data is used unless you add real, authorized data.")

# --------------------------------------------------
# Hero
# --------------------------------------------------

if LOGO_PATH.exists():
    left, right = st.columns([1, 5], vertical_alignment="center")
    with left:
        st.image(str(LOGO_PATH), width=125)
    with right:
        st.markdown(
            """
            <div class="hero">
                <div class="eyebrow">Civic Issue Intelligence</div>
                <div class="hero-title">One issue.<br><span class="accent">One clear priority.</span></div>
                <div class="hero-subtitle">
                    Turn scattered civic complaints into grouped issues and
                    actionable priorities for municipal teams.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Civic Issue Intelligence</div>
            <div class="hero-title">One issue.<br><span class="accent">One clear priority.</span></div>
            <div class="hero-subtitle">
                Turn scattered civic complaints into grouped issues and
                actionable priorities for municipal teams.
            </div>
            <div class="small-muted" style="margin-top:12px">
                Add your logo as <b>civicai_logo.png</b> in the project folder.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Page: Overview
# --------------------------------------------------

if page == "Overview":
    st.markdown('<div class="section-kicker">Live prototype overview</div>', unsafe_allow_html=True)
    st.subheader("Civic issues at a glance")

    total = len(df)
    open_count = int((df["status"].str.lower() != "resolved").sum())
    category_count = int(df["category"].nunique())
    high_urgency = int((df["urgency"] >= 4).sum())

    m1, m2, m3, m4 = st.columns(4)

    metrics = [
        (m1, "Complaints received", total, "Across demo data"),
        (m2, "Issues identified", len(issues), "Grouped issue IDs"),
        (m3, "Needs attention", high_urgency, "Urgency 4 or 5"),
        (m4, "Categories", category_count, "Civic service areas"),
    ]

    for col, label, value, note in metrics:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.15, 1])

    with left:
        st.markdown("### Highest-priority issues")
        if not issues.empty:
            st.dataframe(
                issues[[
                    "Issue ID", "Category", "Complaints",
                    "Priority score", "Status"
                ]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No issues available yet.")

    with right:
        st.markdown("### Complaints by category")
        if not df.empty:
            counts = df["category"].value_counts().rename_axis("Category").reset_index(name="Complaints")
            st.bar_chart(counts.set_index("Category"))
        else:
            st.info("Submit a complaint to begin.")

    st.markdown(
        """
        <div class="info-panel">
            <div class="section-kicker">How CivicAI works</div>
            <b>Ingest → Understand → Cluster → Score → Act</b>
            <p class="small-muted">
                Collect reports, interpret the complaint, group related reports,
                rank the issue, and prepare an officer action.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Page: Report a complaint
# --------------------------------------------------

elif page == "Report a complaint":
    st.markdown('<div class="section-kicker">Community input</div>', unsafe_allow_html=True)
    st.subheader("Report a civic issue")
    st.write("Describe the issue in your own words. This demo saves the report locally.")

    with st.form("complaint_form", clear_on_submit=True):
        complaint_text = st.text_area(
            "Complaint description",
            placeholder="Example: There is a large pothole near the school gate...",
            max_chars=1000,
        )

        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox(
                "Category",
                ["Roads", "Water", "Sanitation", "Streetlights", "Other"],
            )
            urgency = st.slider("Urgency", 1, 5, 3)

        with c2:
            lat = st.number_input("Latitude", value=22.7196, format="%.6f")
            lon = st.number_input("Longitude", value=75.8577, format="%.6f")

        submitted = st.form_submit_button("Submit complaint", use_container_width=True)

    if submitted:
        if len(complaint_text.strip()) < 8:
            st.error("Please enter a little more detail about the issue.")
        else:
            new_id = "C" + uuid.uuid4().hex[:6].upper()

            # Simple demo grouping: assign an existing issue in the same category.
            matching = df[df["category"].str.lower() == category.lower()]
            if not matching.empty:
                issue_id = matching["issue_id"].mode().iloc[0]
            else:
                issue_id = "ISS-" + uuid.uuid4().hex[:4].upper()

            new_row = {
                "id": new_id,
                "text": complaint_text.strip(),
                "category": category,
                "urgency": urgency,
                "lat": lat,
                "lon": lon,
                "date": str(date.today()),
                "issue_id": issue_id,
                "status": "Open",
            }

            updated = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(updated)
            st.success(f"Complaint saved! Reference: {new_id}")
            st.caption("This is local demo storage, not a live municipal submission.")
            st.rerun()

# --------------------------------------------------
# Page: Issue intelligence
# --------------------------------------------------

elif page == "Issue intelligence":
    st.markdown('<div class="section-kicker">Prioritization engine</div>', unsafe_allow_html=True)
    st.subheader("Grouped civic issues")
    st.caption(
        "Priority scores are illustrative. Duration and concentration use demo assumptions; "
        "these weights have not been validated."
    )

    category_filter = st.selectbox(
        "Filter by category",
        ["All categories"] + sorted(df["category"].unique().tolist()),
    )

    filtered = df.copy()
    if category_filter != "All categories":
        filtered = filtered[filtered["category"] == category_filter]

    filtered_issues = make_issue_table(filtered)

    if not filtered_issues.empty:
        st.dataframe(filtered_issues, use_container_width=True, hide_index=True)

        st.markdown("### Why is an issue ranked this way?")
        selected_issue = st.selectbox(
            "Choose an issue",
            filtered_issues["Issue ID"].tolist(),
        )
        group = filtered[filtered["issue_id"] == selected_issue]

        score_volume = round(min(len(group) / 5, 1) * 35, 1)
        score_severity = round((group["urgency"].mean() / 5) * 30, 1)
        score_duration = 10
        score_concentration = round(min(len(group) / 8, 1) * 15, 1)

        with st.expander("View score breakdown", expanded=True):
            st.write(f"**Complaint volume — 35% weight:** {score_volume}/35")
            st.write(f"**Average severity — 30% weight:** {score_severity}/30")
            st.write(f"**Duration — 20% weight:** {score_duration}/20 (demo placeholder)")
            st.write(f"**Concentration — 15% weight:** {score_concentration}/15 (demo proxy)")
            st.progress(min(priority_score(group) / 100, 1.0))
            st.write(f"**Illustrative total:** {priority_score(group)}/100")

            st.markdown("**Related reports**")
            st.dataframe(group[["id", "text", "urgency", "date", "status"]], hide_index=True, use_container_width=True)
    else:
        st.info("No issues match this filter.")

# --------------------------------------------------
# Page: Issue map
# --------------------------------------------------

elif page == "Issue map":
    st.markdown('<div class="section-kicker">Geographic view</div>', unsafe_allow_html=True)
    st.subheader("Where are reports coming from?")
    st.caption("The map uses sample coordinates around Indore. Replace them with verified coordinates for real deployment.")

    map_df = df.dropna(subset=["lat", "lon"]).copy()

    if not map_df.empty:
        color_map = {
            "Roads": [74, 139, 238, 190],
            "Water": [52, 190, 180, 190],
            "Sanitation": [244, 169, 83, 190],
            "Streetlights": [167, 130, 239, 190],
            "Other": [180, 190, 210, 190],
        }

        map_df["color"] = map_df["category"].map(color_map)
        map_df["radius"] = map_df["urgency"].apply(lambda value: 120 + int(value) * 45)

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[lon, lat]",
            get_fill_color="color",
            get_radius="radius",
            pickable=True,
            opacity=0.8,
            stroked=True,
            get_line_color=[220, 235, 255, 180],
            line_width_min_pixels=1,
        )

        view = pdk.ViewState(
            latitude=float(map_df["lat"].mean()),
            longitude=float(map_df["lon"].mean()),
            zoom=12,
            pitch=25,
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view,
            tooltip={
                "html": "<b>{category}</b><br/>{text}<br/>Urgency: {urgency}/5",
                "style": {"backgroundColor": "#172744", "color": "white"},
            },
            map_style=None,
        )

        st.pydeck_chart(deck, use_container_width=True)
        st.caption("Circle size represents urgency. Colours represent categories.")
    else:
        st.info("No valid coordinates available.")

    st.markdown("### Map legend")
    st.write("🔵 Roads   |   🟢 Water   |   🟠 Sanitation   |   🟣 Streetlights")

# --------------------------------------------------
# Page: Officer action
# --------------------------------------------------

elif page == "Officer action":
    st.markdown('<div class="section-kicker">From insight to action</div>', unsafe_allow_html=True)
    st.subheader("Officer action centre")
    st.caption(
        "This is a mock approval workflow. It does not submit complaints to a real government portal."
    )

    if issues.empty:
        st.info("No issues available yet.")
    else:
        chosen = st.selectbox(
            "Select an issue",
            issues["Issue ID"].tolist(),
        )
        selected = issues[issues["Issue ID"] == chosen].iloc[0]
        related = df[df["issue_id"] == chosen]

        st.markdown('<div class="info-panel">', unsafe_allow_html=True)
        st.markdown(f"### {selected['Category']} · {chosen}")
        st.write(selected["Example complaint"])
        st.write(f"**Reports grouped:** {selected['Complaints']}")
        st.write(f"**Illustrative priority:** {selected['Priority score']}/100")
        st.write(f"**Current status:** {selected['Status']}")
        st.markdown("</div>", unsafe_allow_html=True)

        action = st.selectbox(
            "Proposed officer action",
            [
                "Review issue",
                "Assign field inspection",
                "Forward to relevant department",
                "Mark as resolved (demo only)",
            ],
        )

        approved = st.checkbox(
            "I approve this demo action for the selected issue."
        )

        if st.button("Confirm demo action", use_container_width=True):
            if not approved:
                st.warning("Please check the approval box before confirming.")
            else:
                if action == "Mark as resolved (demo only)":
                    df.loc[df["issue_id"] == chosen, "status"] = "Resolved"
                    save_data(df)
                    st.success("Demo status updated to Resolved.")
                    st.rerun()
                else:
                    st.success(f"Demo action recorded: {action}")
                    st.info("No external complaint was filed. Live integration is not configured.")

        with st.expander("View complaints linked to this issue"):
            st.dataframe(
                related[["id", "text", "urgency", "date", "status"]],
                use_container_width=True,
                hide_index=True,
            )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()
st.caption(
    "CivicAI · Prototype for civic issue intelligence · Demo data and provisional scoring · "
    "Not connected to a live municipal system"
)
