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
    layout="centered",
)

# ═══════════════════════════════════════════════════════════════════════════
# CSS STYLING
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }

    /* Hide default Streamlit chrome on the welcome screen for a clean look */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(28, 194, 175, 0.22), transparent 28%),
            radial-gradient(circle at 88% 92%, rgba(245, 158, 11, 0.18), transparent 30%),
            linear-gradient(135deg, #F7FCFB 0%, #EAF8F5 52%, #FFF8E8 100%);
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.3;
        background-image: linear-gradient(120deg, rgba(14, 124, 123, 0.08) 1px, transparent 1px);
        background-size: 34px 34px;
        mask-image: linear-gradient(to bottom right, black, transparent 72%);
    }

    .welcome-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 3.5rem 1rem 1rem 1rem;
        animation: fadeUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(14px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .welcome-logos {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    .welcome-logos img {
        width: min(360px, 82vw);
        height: auto;
        object-fit: contain;
        padding: 0;
        background: transparent;
        border: none;
        box-shadow: none;
    }
    .welcome-plus {
        font-size: 1.5rem;
        color: #94A3B8;
        font-weight: 300;
    }
    .welcome-title h1 {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.01em;
        text-align: center;
    }
    .welcome-title h2 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0E7C7B;
        margin: 0 0 0.5rem 0;
        text-align: center;
    }
    .welcome-title p {
        font-size: 0.9rem;
        color: #64748B;
        margin: 0 0 2rem 0;
        text-align: center;
    }
    .welcome-card {
        background: rgba(255, 255, 255, 0.72);
        backdrop-filter: blur(8px);
        border: 1px solid #CFEFEC;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.75rem;
        width: 100%;
    }
    .welcome-pill {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        text-align: left;
        font-size: 0.88rem;
        font-weight: 600;
        color: #0F172A;
        padding: 0.4rem 0;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #1CC2AF 0%, #0E7C7B 100%);
        border: none;
        border-radius: 14px;
        padding: 0.85rem 2rem;
        font-weight: 700;
        font-size: 1.05rem;
        box-shadow: 0 8px 20px rgba(14, 124, 123, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 26px rgba(14, 124, 123, 0.45);
    }

    .branding-container {
        position: fixed;
        top: 0.75rem;
        right: 0.75rem;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.5rem 0.85rem;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(14, 124, 123, 0.12);
        border: 1px solid rgba(222, 226, 230, 0.7);
    }
    .branding-container img {
        width: 32px; height: 32px; object-fit: contain;
        border-radius: 6px; background: #F8F9FA; padding: 2px;
        border: 1px solid #DEE2E6;
    }
    .branding-text {
        display: flex; flex-direction: column; line-height: 1.2;
        font-size: 0.68rem; white-space: nowrap;
    }
    .branding-text b { color: #0E7C7B; font-size: 0.72rem; }
    .branding-text span { color: #6C757D; }
    @media (max-width: 640px) {
        .welcome-logos img { width: min(300px, 82vw); }
        .welcome-title h1 { font-size: 1.5rem; }
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
                <p>RSUD SLG Kediri &mdash; STIKES Karya Husada Kediri</p>
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

    st.markdown(
        "<p style='text-align:center; color:#94A3B8; font-size:0.78rem; "
        "margin-top:0.75rem;'>Tekan tombol di atas untuk memulai</p>",
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
