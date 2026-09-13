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
            linear-gradient(135deg, #F7FCFB 0%, #EAF8F5 52%, #FFF8E8 100%);
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

    .welcome-wrap {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 1rem 1rem 2rem 1rem;
        animation: fadeUp 0.45s ease;
        width: 100%;
    }
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(14px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .welcome-logos {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 1.2rem;
    }
    .welcome-logos img {
        width: min(760px, 92vw);
        max-height: 60vh;
        height: auto;
        object-fit: contain;
        padding: 0;
        background: transparent;
        border: none;
        box-shadow: none;
        filter: drop-shadow(0 10px 24px rgba(14, 124, 123, 0.08));
    }
    .welcome-title {
        display: none;
    }
    .welcome-card {
        display: none;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #1CC2AF 0%, #0E7C7B 100%);
        border: none;
        border-radius: 16px;
        padding: 0.9rem 2.15rem;
        font-weight: 800;
        font-size: 1.04rem;
        box-shadow: 0 12px 26px rgba(14, 124, 123, 0.28);
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 30px rgba(14, 124, 123, 0.35);
        filter: saturate(1.08);
    }

    @media (max-width: 640px) {
        .welcome-wrap {
            min-height: 100vh;
            padding-top: 0.5rem;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
            justify-content: center;
        }
        .welcome-logos {
            margin-bottom: 0.8rem;
        }
        .welcome-logos img {
            width: min(700px, 92vw);
            max-height: 52vh;
        }
        div[data-testid="stButton"] > button[kind="primary"] {
            width: min(260px, 70vw);
            border-radius: 14px;
            padding: 0.85rem 1rem;
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
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        if st.button(
            "Masuk",
            type="primary",
            icon=":material/arrow_forward:",
            use_container_width=True,
        ):
            st.session_state["entered"] = True
            st.rerun()


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
