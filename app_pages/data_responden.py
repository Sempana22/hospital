"""Tabel seluruh data responden dengan pencarian dan filter."""

import pandas as pd
import streamlit as st

import auth
import database
from utils import JENIS_KELAMIN_OPTIONS, LAMA_DIRAWAT_OPTIONS, QUESTIONS, umur_group

auth.require_admin()

st.markdown("## :material/people: Data Responden")
st.caption("Seluruh jawaban kuesioner yang telah masuk ke database.")

try:
    with st.spinner("Memuat data..."):
        data = database.fetch_responses()
except database.DatabaseConfigError as exc:
    st.error(f":material/error: {exc}")
    st.stop()
except RuntimeError as exc:
    st.error(f":material/error: {exc}")
    st.stop()

if not data:
    st.info(":material/info: Belum ada data responden yang masuk.")
    st.stop()

df = pd.DataFrame(data)
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["created_at"] = df["created_at"].dt.tz_convert("Asia/Jakarta")
df["kelompok_umur"] = df["umur"].apply(umur_group)

c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
with c1:
    search = st.text_input(
        "Cari (nama / kode responden)", placeholder="Ketik untuk mencari..."
    )
with c2:
    jk_filter = st.multiselect("Jenis Kelamin", options=JENIS_KELAMIN_OPTIONS)
with c3:
    lama_filter = st.multiselect("Lama Dirawat", options=LAMA_DIRAWAT_OPTIONS)
with c4:
    umur_filter = st.multiselect("Kelompok Umur", options=sorted(df["kelompok_umur"].unique()))

filtered = df.copy()
if search:
    mask = (
        filtered["respondent_code"].str.contains(search, case=False, na=False)
        | filtered["nama_pasien"].fillna("").str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if jk_filter:
    filtered = filtered[filtered["jenis_kelamin"].isin(jk_filter)]
if lama_filter:
    filtered = filtered[filtered["lama_dirawat"].isin(lama_filter)]
if umur_filter:
    filtered = filtered[filtered["kelompok_umur"].isin(umur_filter)]

st.caption(f"Menampilkan {len(filtered)} dari {len(df)} total responden.")

question_cols = [q for q in QUESTIONS if q in filtered.columns]
display_cols = [
    "respondent_code", "created_at", "nama_pasien", "umur", "jenis_kelamin",
    "lama_dirawat", *question_cols, "saran",
]
display_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered.sort_values("created_at", ascending=False)[display_cols],
    use_container_width=True,
    hide_index=True,
    column_config={
        "created_at": st.column_config.DatetimeColumn("Waktu", format="D MMM YYYY, HH:mm"),
        "respondent_code": "Kode",
        "nama_pasien": "Nama",
        "umur": "Umur",
        "jenis_kelamin": "Jenis Kelamin",
        "lama_dirawat": "Lama Dirawat",
        "saran": "Saran/Kritik",
    },
)

st.divider()
st.markdown("#### :material/delete: Hapus Data Responden")
st.caption("Penghapusan bersifat permanen dan tidak dapat dibatalkan.")

delete_options = filtered.sort_values("created_at", ascending=False).to_dict("records")
selected = st.selectbox(
    "Pilih responden",
    delete_options,
    format_func=lambda row: (
        f"ID {row['id']} | {row.get('nama_pasien') or 'Tanpa nama'} | "
        f"{row['created_at'].strftime('%d %b %Y, %H:%M')}"
    ),
)
confirm_delete = st.checkbox("Saya memahami bahwa data ini akan dihapus permanen.")
if st.button(
    "Hapus Data Terpilih",
    type="secondary",
    icon=":material/delete:",
    disabled=not confirm_delete,
):
    try:
        with st.spinner("Menghapus data..."):
            database.delete_response(int(selected["id"]))
        st.success("Data responden berhasil dihapus.")
        st.rerun()
    except database.DatabaseConfigError as exc:
        st.error(f":material/error: {exc}")
    except RuntimeError as exc:
        st.error(f":material/error: {exc}")
