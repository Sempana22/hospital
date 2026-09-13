"""Main entry point — Navigation and page routing for the hospital survey app."""

import base64
from pathlib import Path

import streamlit as st

from auth import is_admin

# ═══════════════════════════════════════════════════════════════════════════
# KONFIGURASI
# ═══════════════════════════════════════════════════════════════════════════
LOGO_PATH = Path(__file__).with_name("images__1_-removebg-preview.png")
LOGO_DATA_URI = (
    "data:image/png;base64,"
    + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Kuesioner Kepuasan Pasien — RSUD SLG Kediri",
    page_icon=":material/local_hospital:",
    layout="wide",
)

# ═══════════════════════════════════════════════════════════════════════════
# CSS STYLING
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-1: #f5fbfa;
        --bg-2: #ecf9f7;
        --panel: rgba(255,255,255,0.82);
        --primary: #0e7c7b;
        --primary-2: #14a098;
        --primary-3: #7dd3c7;
        --accent: #f59e0b;
        --ink: #0f172a;
        --muted: #52607a;
        --line: rgba(14,124,123,0.14);
        --shadow-soft: 0 16px 40px rgba(15, 23, 42, 0.08);
    }

    * {
        font-family: 'Plus Jakarta Sans', 'Manrope', sans-serif;
        letter-spacing: -0.01em;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(28, 194, 175, 0.18), transparent 28%),
            radial-gradient(circle at 88% 92%, rgba(245, 158, 11, 0.14), transparent 30%),
            linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 52%, #fff9ee 100%);
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.32;
        background-image: linear-gradient(120deg, rgba(14, 124, 123, 0.08) 1px, transparent 1px);
        background-size: 30px 30px;
        mask-image: linear-gradient(to bottom right, black, transparent 72%);
    }
    section.main > div {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        max-width: 1280px !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(6, 41, 40, 0.98), rgba(14, 124, 123, 0.95));
        border-right: 1px solid rgba(255,255,255,0.08);
        box-shadow: 16px 0 32px rgba(6, 40, 39, 0.12);
    }
    [data-testid="stSidebar"] * {
        color: #ecfeff !important;
    }
    section[data-testid="stSidebarContent"] {
        padding: 1rem 0.5rem 0.75rem !important;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 0.5rem;
    }
    [data-testid="stSidebarNav"] > div {
        gap: 0.2rem;
    }
    [data-testid="stSidebarNav"] a {
        border-radius: 14px !important;
        margin: 0.16rem 0.45rem;
        padding: 0.72rem 0.8rem !important;
        transition: all 0.22s ease;
        border: 1px solid transparent;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,255,255,0.12) !important;
        transform: translateX(2px);
        border-color: rgba(255,255,255,0.12);
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255,255,255,0.18) !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.12);
    }
    [data-testid="stSidebarNav"] a span {
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    .stMetric {
        background: rgba(255,255,255,0.7);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1rem 1rem 0.85rem;
        box-shadow: var(--shadow-soft);
    }
    .stMetric .metric-label {
        color: var(--muted) !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
    }
    .stMetric .metric-value {
        color: var(--ink) !important;
        font-size: clamp(1.2rem, 1.8vw, 1.9rem) !important;
        font-weight: 800 !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(14,124,123,0.18);
    }
    div[data-testid="stSpinner"] {
        animation: spinIn 0.4s ease-out;
    }
    div[data-testid="stSpinner"] > div {
        width: 2.1rem !important;
        height: 2.1rem !important;
        border-width: 0.22rem !important;
        border-color: rgba(14,124,123,0.2) !important;
        border-top-color: #0e7c7b !important;
    }
    @keyframes spinIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }

    .welcome-wrap {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0.5rem 1rem 1.5rem 1rem;
        animation: fadeUp 0.45s ease;
    }
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(14px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .welcome-logos {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: -1.5rem;
        margin-bottom: 1.5rem;
        width: 100%;
    }
    .welcome-logos img {
        width: min(640px, 88vw);
        height: auto;
        object-fit: contain;
        padding: 0;
        background: transparent;
        border: none;
        box-shadow: none;
        filter: drop-shadow(0 18px 30px rgba(14, 124, 123, 0.12));
    }
    .welcome-title h1 {
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 800;
        color: #0F172A;
        margin: 0 0 0.45rem 0;
        letter-spacing: -0.02em;
        line-height: 1.08;
        text-align: center;
    }
    .welcome-title h2 {
        font-size: clamp(1.08rem, 2.1vw, 1.4rem);
        font-weight: 700;
        color: #0E7C7B;
        margin: 0 0 0.5rem 0;
        text-align: center;
        letter-spacing: 0.01em;
    }
    .welcome-title p {
        font-size: 0.92rem;
        color: #64748B;
        margin: 0 0 1.75rem 0;
        text-align: center;
        font-weight: 600;
    }
    .welcome-card {
        background: rgba(255, 255, 255, 0.78);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(14, 124, 123, 0.12);
        border-radius: 22px;
        padding: 1.2rem 1rem;
        margin-bottom: 1.5rem;
        width: min(760px, 100%);
        box-shadow: 0 18px 40px rgba(14, 124, 123, 0.08);
    }
    .welcome-pill {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        text-align: left;
        font-size: 0.9rem;
        font-weight: 600;
        color: #1E293B;
        padding: 0.48rem 0.7rem;
        border-radius: 12px;
        background: rgba(14, 124, 123, 0.04);
        margin: 0.2rem 0;
    }
    div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 0 auto;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.55rem;
        background: linear-gradient(135deg, #1CC2AF 0%, #0E7C7B 100%);
        border: none;
        border-radius: 16px;
        padding: 0.92rem 2rem;
        font-weight: 800;
        font-size: 1.04rem;
        box-shadow: 0 12px 26px rgba(14, 124, 123, 0.28);
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        margin: 0 auto;
        min-width: 190px;
        width: min(220px, 72vw);
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 30px rgba(14, 124, 123, 0.35);
        filter: saturate(1.08);
    }

    @media (max-width: 640px) {
        .welcome-wrap {
            min-height: 100vh;
            padding-top: 0.2rem;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
            justify-content: center;
        }
        .welcome-logos {
            margin-top: -2.2rem;
            margin-bottom: 0.8rem;
        }
        .welcome-logos img {
            width: min(500px, 92vw);
        }
        .welcome-title h1 {
            font-size: clamp(1.8rem, 9vw, 2.5rem);
        }
        .welcome-card {
            padding: 0.9rem 0.7rem;
            border-radius: 18px;
        }
        .welcome-pill {
            font-size: 0.82rem;
            padding: 0.45rem 0.55rem;
        }
        div[data-testid="stButton"] > button[kind="primary"] {
            display: block;
            width: auto;
            min-width: 180px;
            margin: 0 auto;
            border-radius: 14px;
            padding: 0.85rem 1.2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_welcome_screen() -> None:
    """A reliable, native welcome screen.

    Uses a real st.button (not a raw HTML/JS button living in an
    iframe) so the click is always caught by Streamlit's own event
    loop — no cross-document JS hacks that can silently fail. Clicking
    "Masuk" flips a session_state flag and reruns straight into the
    kuesioner home page.
    """
    st.markdown(
        f"""
        <div class="welcome-wrap">
            <div class="welcome-logos">
                <img src="{LOGO_DATA_URI}" alt="Logo RSUD SLG Kediri" />
            </div>
            <div class="welcome-title">
                <h1>Kuesioner Kepuasan Pasien</h1>
                <h2>Ruang Anak Rawat Inap Parkit</h2>
                <p>RSUD SLG Kediri</p>
            </div>
            <div class="welcome-card">
                <div class="welcome-pill">⏱️&nbsp; Pengisian singkat, sekitar 3&ndash;5 menit</div>
                <div class="welcome-pill">🔒&nbsp; Data Anda tersimpan aman dan rahasia</div>
                <div class="welcome-pill">💬&nbsp; Saran Anda sangat berarti bagi kami</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_cols = st.columns([1.3, 1.2, 1.3])
    with cta_cols[1]:
        if st.button(
            "Masuk",
            type="primary",
            icon=":material/arrow_forward:",
            use_container_width=True,
            key="welcome_button",
        ):
            st.session_state["entered"] = True
            st.rerun()

    st.markdown(
        "<p style='text-align:center; color:#94A3B8; font-size:0.78rem; "
        "margin-top:0.75rem; margin-bottom:0;'>Tekan tombol di atas untuk memulai</p>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# EKSEKUSI UTAMA
# ═══════════════════════════════════════════════════════════════════════════

if "entered" not in st.session_state:
    st.session_state["entered"] = False

if not st.session_state["entered"]:
    # Welcome / splash screen. No sidebar navigation is shown here so the
    # first thing a visitor sees is the "Masuk" call-to-action.
    st.markdown(
        "<style>[data-testid='stSidebar'] { display: none; }</style>",
        unsafe_allow_html=True,
    )
    render_welcome_screen()
    st.stop()

# From here on the visitor has clicked "Masuk" — show the real app with
# normal sidebar navigation, landing on the kuesioner (home) page.
admin_logged_in = is_admin()

public_pages = [
    st.Page(
        "app_pages/kuesioner.py",
        title="Kuesioner",
        icon=":material/assignment:",
        default=True,
    ),
    st.Page(
        "app_pages/terima_kasih.py",
        title="Terima Kasih",
        icon=":material/check_circle:",
    ),
]

if admin_logged_in:
    admin_pages = [
        st.Page(
            "app_pages/dashboard.py",
            title="Dashboard",
            icon=":material/dashboard:",
        ),
        st.Page(
            "app_pages/data_responden.py",
            title="Data Responden",
            icon=":material/people:",
        ),
        st.Page(
            "app_pages/statistik.py",
            title="Statistik",
            icon=":material/analytics:",
        ),
        st.Page(
            "app_pages/saran_kritik.py",
            title="Saran & Kritik",
            icon=":material/feedback:",
        ),
        st.Page(
            "app_pages/export_data.py",
            title="Export Data",
            icon=":material/download:",
        ),
        st.Page(
            "app_pages/admin_login.py",
            title="Logout",
            icon=":material/logout:",
        ),
    ]
else:
    admin_pages = [
        st.Page(
            "app_pages/admin_login.py",
            title="Login Admin",
            icon=":material/lock:",
        ),
    ]

nav_sections = {
    "": public_pages,
    "Admin": admin_pages,
}

page = st.navigation(nav_sections, position="sidebar")
page.run()
