
import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

# =========================================================
# CIVICAI CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CivicAI | Smart Civic Portal",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "complaints.csv")
UPLOAD_DIR = "uploads"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================================================
# PASTEL THEME AND ANIMATIONS - ORIGINAL INTERFACE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #26364a;
    --muted: #65758b;
    --blue: #7399d4;
    --teal: #68b9ad;
    --lavender: #b5a8e8;
    --pink: #e9b7ca;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 5%, #e4eee8 0%, transparent 38%),
        radial-gradient(ellipse at 95% 8%, #e6e3fa 0%, transparent 35%),
        radial-gradient(ellipse at 50% 100%, #f7e8ef 0%, transparent 42%),
        linear-gradient(135deg, #f2f6f0, #eef1fb 55%, #fbf0f3);
    background-attachment: fixed;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    color: #26364a !important;
}

.hero {
    padding: 34px;
    border-radius: 28px;
    background: linear-gradient(
        120deg,
        rgba(255,255,255,.82),
        rgba(225,238,246,.78),
        rgba(239,230,250,.78)
    );
    border: 1px solid rgba(255,255,255,.85);
    box-shadow: 0 14px 40px rgba(72,91,126,.10);
    animation: fadeUp .7s ease-out;
    margin-bottom: 24px;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #26364a;
}

.hero-title span {
    background: linear-gradient(90deg, #5a91c9, #62afa4, #9c8bda);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #65758b;
    font-size: 1.05rem;
    line-height: 1.7;
}

.section-label {
    color: #638b91;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.soft-card {
    background: rgba(255,255,255,.74);
    border: 1px solid rgba(255,255,255,.9);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 8px 26px rgba(72,91,126,.07);
    transition: transform .25s ease, box-shadow .25s ease;
    margin-bottom: 14px;
}

.soft-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 32px rgba(72,91,126,.12);
}

.metric-card {
    background: rgba(255,255,255,.78);
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 7px 22px rgba(72,91,126,.07);
    animation: fadeUp .5s ease-out;
}

.metric-label {
    color: #65758b;
    font-size: .88rem;
    font-weight: 600;
}

.metric-value {
    color: #26364a;
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 5px;
}

.pill {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 99px;
    background: #e0f0e9;
    color: #397a6c;
    font-size: .78rem;
    font-weight: 700;
}

.stButton > button {
    border: 0;
    border-radius: 13px;
    padding: .62rem 1.1rem;
    background: linear-gradient(100deg, #72b9ac, #80a9dc);
    color: white;
    font-weight: 700;
    transition: all .2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(87,151,162,.25);
    color: white;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
textarea {
    background: rgba(255,255,255,.8) !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e3eee8, #e9e7f8, #f7e9ef);
    border-right: 1px solid rgba(255,255,255,.8);
}

[data-testid="stSidebar"] * {
    color: #26364a;
}

div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

hr {
    border-color: rgba(116,137,165,.18);
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-7px); }
}

.float-icon {
    display: inline-block;
    animation: float 3s ease-in-out infinite;
    font-size: 3rem;
}

.footer {
    text-align: center;
    padding: 22px 0 5px;
    color: #78869a;
    font-size: .82rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA MANAGEMENT
# =========================================================

COLUMNS = [
    "complaint_id",
    "title",
    "description",
    "category",
    "location",
    "priority",
    "status",
    "submitted_by",
    "created_at",
    "officer_note",
    "photo_path",
]


def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_csv(DATA_FILE)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=COLUMNS)

    # Add new columns to older CSV files automatically.
    for column in COLUMNS:
        if column not in df.columns:
            df[column] = ""

    return df


def save_data(df):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(DATA_FILE, index=False)


def create_demo_data():
    rows = [
        {
            "complaint_id": "CA-1001",
            "title": "Garbage not collected",
            "description": "Garbage has accumulated near the main road.",
            "category": "Waste Management",
            "location": "Bhawarkua, Indore",
            "priority": "High",
            "status": "Submitted",
            "submitted_by": "demo",
            "created_at": "2026-10-20 09:30",
            "officer_note": "",
            "photo_path": "",
        },
        {
            "complaint_id": "CA-1002",
            "title": "Streetlight not working",
            "description": "Streetlight near the residential lane is not working.",
            "category": "Streetlights",
            "location": "Vijay Nagar, Indore",
            "priority": "Medium",
            "status": "In Progress",
            "submitted_by": "demo",
            "created_at": "2026-10-21 18:10",
            "officer_note": "Inspection requested.",
            "photo_path": "",
        },
        {
            "complaint_id": "CA-1003",
            "title": "Water leakage",
            "description": "Water is leaking from a roadside pipeline.",
            "category": "Water Supply",
            "location": "Palasia, Indore",
            "priority": "High",
            "status": "Submitted",
            "submitted_by": "demo",
            "created_at": "2026-10-22 11:15",
            "officer_note": "",
            "photo_path": "",
        },
        {
            "complaint_id": "CA-1004",
            "title": "Road damage",
            "description": "Potholes are causing problems for commuters.",
            "category": "Roads",
            "location": "Rajendra Nagar, Indore",
            "priority": "Low",
            "status": "Resolved",
            "submitted_by": "demo",
            "created_at": "2026-10-18 14:20",
            "officer_note": "Repair marked complete in demo.",
            "photo_path": "",
        },
    ]

    return pd.DataFrame(rows, columns=COLUMNS)


def initialize_data():
    if not os.path.exists(DATA_FILE):
        save_data(create_demo_data())


initialize_data()

# =========================================================
# PRIORITY SCORING
# =========================================================

def calculate_priority(category, description):
    text = f"{category} {description}".lower()

    urgent_words = [
        "emergency", "danger", "accident", "severe",
        "overflow", "exposed wire", "unsafe", "urgent",
    ]

    high_words = [
        "leak", "blocked", "broken", "garbage",
        "pothole", "water", "damage", "not working",
    ]

    if any(word in text for word in urgent_words):
        return "High"

    if any(word in text for word in high_words):
        return "High"

    return "Medium"


def make_complaint_id(df):
    existing = (
        set(df["complaint_id"].astype(str))
        if not df.empty else set()
    )

    while True:
        new_id = f"CA-{uuid.uuid4().hex[:6].upper()}"
        if new_id not in existing:
            return new_id


def safe_string(value):
    if pd.isna(value):
        return ""
    return str(value)


def show_complaint_photo(row, heading="📷 Attached photo"):
    """Display an attached photo if its file exists."""
    photo_path = safe_string(row.get("photo_path", ""))

    if photo_path and os.path.isfile(photo_path):
        st.subheader(heading)
        st.image(
            photo_path,
            caption=f"Complaint {safe_string(row.get('complaint_id', ''))}",
            use_container_width=True,
        )
    else:
        st.caption("No photo attached to this complaint.")


# =========================================================
# LOGIN AND SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "login_choice" not in st.session_state:
    st.session_state.login_choice = None


# Demo-only accounts. Do not use these as production credentials.
DEMO_USERS = {
    "citizen": {
        "password": "citizen123",
        "role": "Citizen",
    },
    "officer": {
        "password": "officer123",
        "role": "Officer",
    },
}


def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.page = "Home"
    st.session_state.login_choice = None
    st.rerun()


def login_screen():
    st.markdown("""
    <div class="hero">
        <div class="section-label">WELCOME TO CIVICAI</div>
        <div class="hero-title">Your city.<br><span>Your voice.</span></div>
        <p class="subtitle">
            A smarter way to report civic problems, track complaints,
            and help make neighbourhoods better.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("""
        <div class="soft-card">
            <div class="float-icon">🌿</div>
            <h2>Citizen Portal</h2>
            <p>Report civic issues, track your complaints,
            and stay updated on their progress.</p>
            <span class="pill">For residents</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Continue as Citizen →",
            key="citizen_choice",
            use_container_width=True,
        ):
            st.session_state.login_choice = "Citizen"

    with right:
        st.markdown("""
        <div class="soft-card">
            <div class="float-icon">🏛️</div>
            <h2>Officer Portal</h2>
            <p>Review complaints, monitor issue trends,
            and update complaint resolution status.</p>
            <span class="pill">For civic officers</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Continue as Officer →",
            key="officer_choice",
            use_container_width=True,
        ):
            st.session_state.login_choice = "Officer"

    choice = st.session_state.login_choice

    if choice:
        st.divider()
        st.subheader(f"🔐 {choice} Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if submitted:
            username_key = username.strip().lower()
            user = DEMO_USERS.get(username_key)

            if (
                user
                and user["password"] == password
                and user["role"] == choice
            ):
                st.session_state.authenticated = True
                st.session_state.role = user["role"]
                st.session_state.username = username_key
                st.session_state.page = (
                    "My dashboard"
                    if choice == "Citizen"
                    else "Overview"
                )
                st.rerun()
            else:
                st.error("Invalid credentials for this portal.")

        st.info(
            "Demo credentials: citizen / citizen123 or "
            "officer / officer123. These are only for local testing."
        )

    st.markdown("""
    <div class="footer">
        CivicAI • Prototype for smarter, more responsive cities
    </div>
    """, unsafe_allow_html=True)


# Display login page before authentication.
if not st.session_state.authenticated:
    login_screen()
    st.stop()


# =========================================================
# SIDEBAR AND NAVIGATION
# =========================================================

role = st.session_state.role
username = st.session_state.username
df = load_data()

st.sidebar.markdown("""
<div style="padding:8px 0 18px 0;">
    <div style="font-size:2rem;">🏙️</div>
    <h2 style="margin:0;">CivicAI</h2>
    <p style="color:#65758b; margin-top:4px;">
        Smart Civic Portal
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write(f"👤 **{username}**")
st.sidebar.caption(f"Signed in as {role}")

if role == "Citizen":
    pages = [
        "My dashboard",
        "Report a complaint",
        "My complaints",
    ]
else:
    pages = [
        "Overview",
        "Issue intelligence",
        "Issue map",
        "Officer action",
        "All complaints",
    ]

if st.session_state.page not in pages:
    st.session_state.page = pages[0]

page = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page),
)
st.session_state.page = page

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Log out", use_container_width=True):
    logout()

st.sidebar.caption("CivicAI prototype • Local CSV storage")


# =========================================================
# REUSABLE UI FUNCTIONS
# =========================================================

def metric_card(label, value, icon):
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:1.5rem;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_metrics(data):
    total = len(data)

    if total:
        open_count = int((data["status"] != "Resolved").sum())
        resolved_count = int((data["status"] == "Resolved").sum())
        high_count = int((data["priority"] == "High").sum())
    else:
        open_count = resolved_count = high_count = 0

    a, b, c, d = st.columns(4)

    with a:
        metric_card("Total complaints", total, "📋")
    with b:
        metric_card("Open complaints", open_count, "⏳")
    with c:
        metric_card("Resolved", resolved_count, "✅")
    with d:
        metric_card("High priority", high_count, "🚨")


def show_complaints_table(data):
    if data.empty:
        st.info("No complaints found.")
        return

    display_columns = [
        "complaint_id",
        "title",
        "category",
        "location",
        "priority",
        "status",
        "created_at",
    ]

    available_columns = [
        col for col in display_columns if col in data.columns
    ]

    st.dataframe(
        data[available_columns],
        use_container_width=True,
        hide_index=True,
    )


def status_badge(status):
    icons = {
        "Submitted": "🟡",
        "In Progress": "🔵",
        "Resolved": "🟢",
    }
    return f"{icons.get(status, '⚪')} {status}"


# =========================================================
# CITIZEN PORTAL
# =========================================================

if role == "Citizen":

    if page == "My dashboard":
        st.markdown("""
        <div class="hero">
            <div class="section-label">CITIZEN SPACE</div>
            <div class="hero-title">Hello, <span>neighbour!</span> 👋</div>
            <p class="subtitle">
                Your voice can make a difference. Report an issue
                and help your community move forward.
            </p>
        </div>
        """, unsafe_allow_html=True)

        my_data = df[
            df["submitted_by"].astype(str).str.lower()
            == username.lower()
        ].copy()

        show_metrics(my_data)

        st.subheader("📌 Your recent complaints")
        show_complaints_table(
            my_data.sort_values(
                "created_at", ascending=False
            ).head(5)
        )

        if st.button("➕ Report a new issue"):
            st.session_state.page = "Report a complaint"
            st.rerun()

    elif page == "Report a complaint":
        st.markdown("""
        <div class="hero">
            <div class="section-label">MAKE YOUR VOICE HEARD</div>
            <div class="hero-title">Report an <span>issue.</span></div>
            <p class="subtitle">
                Share accurate details so the relevant team can
                review your complaint.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------
        # NEW: PHOTO CAPTURE / UPLOAD
        # -------------------------------------------------

        st.subheader("📷 Attach a photo (optional)")

        photo_option = st.radio(
            "Choose how to add a photo",
            ["No photo", "Take a live photo", "Upload a photo"],
            horizontal=True,
            key="photo_option",
        )

        photo = None

        if photo_option == "Take a live photo":
            photo = st.camera_input(
                "Take a picture of the civic issue",
                key="complaint_camera",
            )

        elif photo_option == "Upload a photo":
            photo = st.file_uploader(
                "Choose an image from your device",
                type=["jpg", "jpeg", "png"],
                key="complaint_upload",
                help="Supported formats: JPG, JPEG and PNG.",
            )

        if photo is not None:
            if photo.size > 10 * 1024 * 1024:
                st.error("Image must be smaller than 10 MB.")
                photo = None
            else:
                st.image(
                    photo,
                    caption="Photo preview",
                    use_container_width=True,
                )

        # -------------------------------------------------
        # EXISTING COMPLAINT FORM
        # -------------------------------------------------

        with st.form("complaint_form", clear_on_submit=True):
            title = st.text_input(
                "Complaint title",
                placeholder="e.g. Streetlight not working",
            )

            category = st.selectbox(
                "Issue category",
                [
                    "Roads",
                    "Waste Management",
                    "Water Supply",
                    "Streetlights",
                    "Drainage",
                    "Public Safety",
                    "Other",
                ],
            )

            location = st.text_input(
                "Location",
                placeholder="Area, street, or nearby landmark",
            )

            description = st.text_area(
                "Describe the problem",
                placeholder="Explain what happened and where...",
                height=140,
            )

            submitted = st.form_submit_button(
                "📨 Submit complaint",
                use_container_width=True,
            )

        if submitted:
            if (
                not title.strip()
                or not location.strip()
                or not description.strip()
            ):
                st.error(
                    "Please fill in the title, location, and description."
                )

            elif photo_option != "No photo" and photo is None:
                st.error(
                    "Please capture or upload a valid image, "
                    "or select No photo."
                )

            else:
                current_df = load_data()
                priority = calculate_priority(category, description)
                complaint_id = make_complaint_id(current_df)
                photo_path = ""

                # Save the image using the complaint ID.
                if photo is not None:
                    extension = (
                        ".png"
                        if photo.type == "image/png"
                        else ".jpg"
                    )

                    image_filename = f"{complaint_id}{extension}"
                    destination = os.path.join(
                        UPLOAD_DIR,
                        image_filename,
                    )

                    with open(destination, "wb") as image_file:
                        image_file.write(photo.getvalue())

                    photo_path = destination

                new_complaint = {
                    "complaint_id": complaint_id,
                    "title": title.strip(),
                    "description": description.strip(),
                    "category": category,
                    "location": location.strip(),
                    "priority": priority,
                    "status": "Submitted",
                    "submitted_by": username,
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "officer_note": "",
                    "photo_path": photo_path,
                }

                updated_df = pd.concat(
                    [
                        current_df,
                        pd.DataFrame([new_complaint]),
                    ],
                    ignore_index=True,
                )

                save_data(updated_df)

                st.success(
                    "Complaint submitted successfully! "
                    f"Your complaint ID is {complaint_id}."
                )

                if photo_path:
                    st.success(
                        "Your photo has been attached to the complaint."
                    )

                st.info(f"Suggested priority: {priority}")

                # Clear the photo widgets after successful submission.
                st.session_state.pop("complaint_camera", None)
                st.session_state.pop("complaint_upload", None)
                st.session_state.pop("photo_option", None)

    elif page == "My complaints":
        st.markdown("""
        <div class="hero">
            <div class="section-label">YOUR ACTIVITY</div>
            <div class="hero-title">My <span>complaints.</span></div>
            <p class="subtitle">
                Track the progress of issues submitted through your account.
            </p>
        </div>
        """, unsafe_allow_html=True)

        my_data = df[
            df["submitted_by"].astype(str).str.lower()
            == username.lower()
        ].copy()

        if not my_data.empty:
            status_filter = st.selectbox(
                "Filter by status",
                ["All", "Submitted", "In Progress", "Resolved"],
            )

            if status_filter != "All":
                my_data = my_data[
                    my_data["status"] == status_filter
                ]

        show_complaints_table(
            my_data.sort_values("created_at", ascending=False)
        )

        if not my_data.empty:
            st.subheader("Complaint details")

            selected_id = st.selectbox(
                "Select complaint ID",
                my_data["complaint_id"].astype(str).tolist(),
            )

            selected = my_data[
                my_data["complaint_id"].astype(str) == selected_id
            ].iloc[0]

            show_complaint_photo(
                selected,
                heading="📷 Your attached photo",
            )

            st.markdown(f"""
            <div class="soft-card">
                <h3>{safe_string(selected['title'])}</h3>
                <p><b>Complaint ID:</b>
                    {safe_string(selected['complaint_id'])}</p>
                <p><b>Category:</b>
                    {safe_string(selected['category'])}</p>
                <p><b>Location:</b>
                    {safe_string(selected['location'])}</p>
                <p><b>Status:</b>
                    {status_badge(safe_string(selected['status']))}</p>
                <p><b>Description:</b>
                    {safe_string(selected['description'])}</p>
                <p><b>Officer note:</b>
                    {safe_string(selected['officer_note']) or 'No update yet.'}</p>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# OFFICER PORTAL
# =========================================================

elif role == "Officer":

    if page == "Overview":
        st.markdown("""
        <div class="hero">
            <div class="section-label">OFFICER WORKSPACE</div>
            <div class="hero-title">City <span>overview.</span> 🏛️</div>
            <p class="subtitle">
                Monitor citizen complaints, identify urgent issues,
                and track resolution progress.
            </p>
        </div>
        """, unsafe_allow_html=True)

        show_metrics(df)

        st.subheader("📋 Latest complaints")
        show_complaints_table(
            df.sort_values("created_at", ascending=False).head(10)
        )

        st.subheader("📊 Complaints by status")
        if not df.empty:
            st.bar_chart(df["status"].value_counts())

        st.subheader("📍 Complaints by category")
        if not df.empty:
            st.bar_chart(df["category"].value_counts())

    elif page == "Issue intelligence":
        st.markdown("""
        <div class="hero">
            <div class="section-label">DATA-DRIVEN DECISIONS</div>
            <div class="hero-title">Issue <span>intelligence.</span></div>
            <p class="subtitle">
                Explore recurring civic problems and understand
                where attention may be needed.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if df.empty:
            st.info("There are no complaints to analyse yet.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Category distribution")
                st.bar_chart(df["category"].value_counts())

            with col2:
                st.subheader("Priority distribution")
                st.bar_chart(df["priority"].value_counts())

            st.subheader("Status distribution")
            st.bar_chart(df["status"].value_counts())

            st.subheader("Repeated locations")

            location_counts = (
                df.groupby("location")
                .size()
                .reset_index(name="complaint_count")
                .sort_values("complaint_count", ascending=False)
            )

            st.dataframe(
                location_counts,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Summaries are based on complaints stored in the CSV file."
            )

    elif page == "Issue map":
        st.markdown("""
        <div class="hero">
            <div class="section-label">LOCATION AWARENESS</div>
            <div class="hero-title">Issue <span>map.</span> 🗺️</div>
            <p class="subtitle">
                Review the reported locations of civic issues.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if df.empty:
            st.info("No complaint locations are available.")
        else:
            st.warning(
                "This prototype uses location names, not verified GPS "
                "coordinates. This page shows a location list and "
                "frequency chart, not a geographic heat map."
            )

            st.dataframe(
                df[[
                    "complaint_id",
                    "title",
                    "category",
                    "location",
                    "priority",
                    "status",
                ]],
                use_container_width=True,
                hide_index=True,
            )

            st.subheader("Location frequency")

            location_counts = (
                df.groupby("location")
                .size()
                .reset_index(name="complaint_count")
                .sort_values("complaint_count", ascending=False)
            )

            st.bar_chart(
                location_counts.set_index("location")["complaint_count"]
            )

    elif page == "Officer action":
        st.markdown("""
        <div class="hero">
            <div class="section-label">COMPLAINT MANAGEMENT</div>
            <div class="hero-title">Officer <span>actions.</span></div>
            <p class="subtitle">
                Update complaint status and record an action note.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if df.empty:
            st.info("There are no complaints to update.")
        else:
            complaint_ids = df["complaint_id"].astype(str).tolist()

            selected_id = st.selectbox(
                "Select complaint",
                complaint_ids,
            )

            row_index = df.index[
                df["complaint_id"].astype(str) == selected_id
            ][0]

            selected = df.loc[row_index]

            st.markdown(f"""
            <div class="soft-card">
                <h3>{safe_string(selected['title'])}</h3>
                <p><b>Location:</b>
                    {safe_string(selected['location'])}</p>
                <p><b>Category:</b>
                    {safe_string(selected['category'])}</p>
                <p><b>Priority:</b>
                    {safe_string(selected['priority'])}</p>
                <p><b>Description:</b>
                    {safe_string(selected['description'])}</p>
            </div>
            """, unsafe_allow_html=True)

            # NEW: Show the photo attached by the citizen.
            show_complaint_photo(
                selected,
                heading="📷 Citizen-submitted photo",
            )

            current_status = safe_string(selected["status"])
            status_options = ["Submitted", "In Progress", "Resolved"]

            if current_status not in status_options:
                status_options.append(current_status)

            current_note = safe_string(selected["officer_note"])

            with st.form("officer_action_form"):
                new_status = st.selectbox(
                    "Update status",
                    status_options,
                    index=status_options.index(current_status),
                )

                officer_note = st.text_area(
                    "Officer action note",
                    value=current_note,
                    placeholder="Add action or resolution details...",
                )

                save_action = st.form_submit_button(
                    "💾 Save update",
                    use_container_width=True,
                )

            if save_action:
                updated_df = load_data()
                match = (
                    updated_df["complaint_id"].astype(str) == selected_id
                )

                updated_df.loc[match, "status"] = new_status
                updated_df.loc[match, "officer_note"] = officer_note.strip()

                save_data(updated_df)
                st.success("Complaint update saved.")
                st.rerun()

    elif page == "All complaints":
        st.markdown("""
        <div class="hero">
            <div class="section-label">COMPLAINT DIRECTORY</div>
            <div class="hero-title">All <span>complaints.</span></div>
            <p class="subtitle">
                Search, filter, and review complaints submitted to CivicAI.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if df.empty:
            st.info("No complaints have been submitted.")
        else:
            search_text = st.text_input(
                "🔎 Search complaints",
                placeholder="Search by ID, title, category, or location...",
            )

            filtered = df.copy()

            if search_text.strip():
                query = search_text.strip().lower()

                searchable = (
                    filtered["complaint_id"].astype(str)
                    + " "
                    + filtered["title"].astype(str)
                    + " "
                    + filtered["category"].astype(str)
                    + " "
                    + filtered["location"].astype(str)
                ).str.lower()

                filtered = filtered[
                    searchable.str.contains(query, na=False)
                ]

            col1, col2 = st.columns(2)

            with col1:
                status_filter = st.selectbox(
                    "Status",
                    ["All", "Submitted", "In Progress", "Resolved"],
                )

            with col2:
                priority_filter = st.selectbox(
                    "Priority",
                    ["All", "High", "Medium", "Low"],
                )

            if status_filter != "All":
                filtered = filtered[
                    filtered["status"] == status_filter
                ]

            if priority_filter != "All":
                filtered = filtered[
                    filtered["priority"] == priority_filter
                ]

            st.write(f"Showing **{len(filtered)}** complaint(s).")
            show_complaints_table(filtered)

            csv_data = filtered.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Export filtered complaints as CSV",
                data=csv_data,
                file_name="civicai_complaints.csv",
                mime="text/csv",
                use_container_width=True,
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    CivicAI • A smart civic complaint management prototype<br>
    Demo authentication and local CSV storage are intended for testing only.
</div>
""", unsafe_allow_html=True)
