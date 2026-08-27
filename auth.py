"""Admin authentication module using session state and secrets."""

import streamlit as st


def verify_admin(username: str, password: str) -> bool:
    """Verify admin credentials against Streamlit secrets."""
    try:
        correct_user = st.secrets["ADMIN_USERNAME"]
        correct_pass = st.secrets["ADMIN_PASSWORD"]
        return username == correct_user and password == correct_pass
    except (KeyError, FileNotFoundError):
        return False


def login_admin() -> bool:
    """Attempt admin login. Returns True if already logged in or login succeeds."""
    if st.session_state.get("admin_logged_in"):
        return True

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align:center; margin-bottom: 0.5rem;">
                <div style="font-size:2.5rem;">🔐</div>
                <h3 style="margin-bottom:0;">Login Admin</h3>
                <p style="color:#6C757D; font-size:0.9rem;">
                    Masuk untuk mengakses dashboard pengelolaan data.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", border=True):
            username = st.text_input(
                "Username",
                placeholder="Masukkan username",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Masukkan password",
            )
            submitted = st.form_submit_button(
                "Masuk", type="primary", icon=":material/login:", use_container_width=True
            )

        if submitted:
            if not username or not password:
                st.warning("Username dan password harus diisi.")
                return False
            if verify_admin(username, password):
                st.session_state["admin_logged_in"] = True
                st.toast("Login berhasil!", icon=":material/check_circle:")
                st.rerun()
            else:
                st.error("Username atau password salah. Silakan coba kembali.")
                return False

    return False


def logout_admin():
    """Log out the admin."""
    st.session_state.pop("admin_logged_in", None)
    st.rerun()


def is_admin() -> bool:
    """Check if current session is authenticated as admin."""
    return st.session_state.get("admin_logged_in", False)


def require_admin():
    """Stop rendering the current page unless the session is admin-authenticated.

    Call this at the very top of any admin-only page.
    """
    if not is_admin():
        st.warning(
            ":material/lock: Halaman ini khusus admin. Silakan login terlebih dahulu."
        )
        if st.button("Ke Halaman Login", icon=":material/login:"):
            st.switch_page("app_pages/admin_login.py")
        st.stop()
