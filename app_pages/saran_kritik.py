"""Daftar saran dan kritik dari responden."""

import pandas as pd
import streamlit as st

import auth
import database

auth.require_admin()

st.markdown("## :material/feedback: Saran & Kritik")
st.caption("Masukan bebas dari pasien/orang tua/wali pasien.")

try:
    with st.spinner("Memuat data..."):
        feedback = database.fetch_feedback()
except database.DatabaseConfigError as exc:
    st.error(f":material/error: {exc}")
    st.stop()
except RuntimeError as exc:
    st.error(f":material/error: {exc}")
    st.stop()

if not feedback:
    st.info(":material/info: Belum ada saran atau kritik yang masuk.")
    st.stop()

df = pd.DataFrame(feedback)
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["created_at"] = df["created_at"].dt.tz_convert("Asia/Jakarta")

search = st.text_input("Cari dalam saran", placeholder="Ketik kata kunci...")
filtered = df
if search:
    filtered = df[df["saran"].str.contains(search, case=False, na=False)]

st.caption(f"Menampilkan {len(filtered)} dari {len(df)} saran/kritik.")

for _, row in filtered.sort_values("created_at", ascending=False).iterrows():
    tanggal = row["created_at"].strftime("%d %b %Y, %H:%M") if pd.notna(row["created_at"]) else "-"
    st.markdown(
        f"""
        <div style="background:#F8FAFC; border-left:4px solid #0E7C7B; border-radius:10px;
                    padding:0.9rem 1.1rem; margin-bottom:0.75rem;">
            <div style="font-size:0.78rem; color:#64748B; margin-bottom:0.35rem;">
                <b>{row['respondent_code']}</b> &middot; {tanggal}
            </div>
            <div style="color:#0F172A;">{row['saran']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
