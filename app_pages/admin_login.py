"""Halaman login/logout admin."""

import streamlit as st

import auth

st.markdown(
    """
    <style>
    .admin-hero {
        background: linear-gradient(135deg, #0E7C7B 0%, #14A098 100%);
        border-radius: 20px;
        padding: 1.4rem 1.5rem;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 18px 38px rgba(14, 124, 123, 0.22);
    }
    .admin-hero h1 {
        font-size: clamp(1.2rem, 2vw, 1.7rem);
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .admin-status {
        background: rgba(255,255,255,0.76);
        border: 1px solid rgba(14, 124, 123, 0.12);
        border-radius: 18px;
        padding: 1rem 1.2rem;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
    }
    </style>
    <div class="admin-hero"><h1>🔐 Area Admin — RSUD SLG Kediri</h1></div>
    """,
    unsafe_allow_html=True,
)

if auth.is_admin():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success(":material/check_circle: Anda sudah login sebagai admin.")
        st.markdown(
            '<div class="admin-status">Gunakan menu di sidebar untuk membuka <strong>Dashboard</strong>, '
            '<strong>Data Responden</strong>, <strong>Statistik</strong>, <strong>Saran & Kritik</strong>, '
            'atau <strong>Export Data</strong>.</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Logout", type="secondary", icon=":material/logout:", use_container_width=True
        ):
            auth.logout_admin()
else:
    auth.login_admin()
