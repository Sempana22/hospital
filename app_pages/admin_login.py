"""Halaman login/logout admin."""

import streamlit as st

import auth

st.markdown(
    """
    <style>
    .admin-hero {
        background: linear-gradient(135deg, #0E7C7B 0%, #14A098 100%);
        border-radius: 16px; padding: 1.25rem 1.5rem; color: white;
        margin-bottom: 1.5rem; text-align: center;
    }
    .admin-hero h1 { font-size: 1.2rem; margin: 0; font-weight: 700; }
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
            "Gunakan menu di sidebar untuk membuka **Dashboard**, "
            "**Data Responden**, **Statistik**, **Saran & Kritik**, atau **Export Data**."
        )
        if st.button(
            "Logout", type="secondary", icon=":material/logout:", use_container_width=True
        ):
            auth.logout_admin()
else:
    auth.login_admin()
