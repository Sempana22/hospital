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

    st.markdown(
        """
        <style>
        .admin-shell {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 82vh;
            padding: 1rem 0;
        }
        .admin-panel {
            width: min(520px, 100%);
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(14,124,123,0.12);
            border-radius: 26px;
            padding: 2rem 1.5rem 1.5rem;
            box-shadow: 0 22px 50px rgba(15,23,42,0.08);
            backdrop-filter: blur(8px);
        }
        .admin-panel h3 {
            margin: 0.35rem 0 0.35rem;
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 800;
            color: #0f172a;
            text-align: center;
        }
        .admin-panel p {
            color: #5b6b82;
            font-size: 0.9rem;
            text-align: center;
            margin: 0 0 1.1rem;
        }
        .admin-badge {
            width: 74px;
            height: 74px;
            border-radius: 20px;
            background: linear-gradient(135deg, #0e7c7b, #14a098);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.9rem;
            font-size: 2rem;
            box-shadow: 0 16px 32px rgba(14,124,123,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="admin-shell"><div class="admin-panel">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="admin-badge">🔐</div>
        <h3>Login Admin</h3>
        <p>Masuk untuk mengakses dashboard pengelolaan data.</p>
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
            st.markdown('</div></div>', unsafe_allow_html=True)
            return False
        if verify_admin(username, password):
            st.session_state["admin_logged_in"] = True
            st.toast("Login berhasil!", icon=":material/check_circle:")
            st.rerun()
        else:
            st.error("Username atau password salah. Silakan coba kembali.")
            st.markdown('</div></div>', unsafe_allow_html=True)
            return False

    st.markdown('</div></div>', unsafe_allow_html=True)
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
