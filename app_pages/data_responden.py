"""Tabel seluruh data responden dengan pencarian dan filter."""

import pandas as pd
import streamlit as st

import auth
import database
from utils import JENIS_KELAMIN_OPTIONS, LAMA_DIRAWAT_OPTIONS, QUESTIONS, format_umur, umur_group

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
if "umur_satuan" not in df.columns:
    df["umur_satuan"] = "tahun"
df["umur_satuan"] = df["umur_satuan"].fillna("tahun").astype(str).str.strip().str.lower()
df["kelompok_umur"] = df.apply(lambda r: umur_group(r["umur"], r.get("umur_satuan", "tahun")), axis=1)
df["umur_display"] = df.apply(
    lambda r: format_umur(r.get("umur"), r.get("umur_satuan", "tahun")),
    axis=1,
)

st.markdown(
    """
    <style>
    .table-card {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(14, 124, 123, 0.06);
        margin-bottom: 1.5rem;
    }
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(14, 124, 123, 0.04);
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        max-height: none !important;
        border: 1px solid rgba(15, 23, 42, 0.06);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.98);
    }
    .stDataFrame .dataframe {
        width: 100% !important;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 12px;
    }
    .stDataFrame .dataframe thead th {
        background: rgba(14, 124, 123, 0.08);
        color: #0f172a;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
        padding: 0.8rem 0.75rem;
        border-bottom: 2px solid rgba(14, 124, 123, 0.12);
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .stDataFrame .dataframe th:first-child {
        border-top-left-radius: 10px;
    }
    .stDataFrame .dataframe th:last-child {
        border-top-right-radius: 10px;
    }
    .stDataFrame .dataframe td {
        vertical-align: middle;
        padding: 0.55rem 0.75rem;
        font-size: 12px;
        border-bottom: 1px solid rgba(15, 23, 42, 0.04);
        color: #1e293b;
    }
    .stDataFrame .dataframe tbody tr:hover {
        background: rgba(14, 124, 123, 0.03);
    }
    .stDataFrame .dataframe tbody tr:last-child td {
        border-bottom: none;
    }
    .stDataFrame .dataframe td:first-child {
        border-bottom-left-radius: 8px;
    }
    .stDataFrame .dataframe td:last-child {
        border-bottom-right-radius: 8px;
    }
    .filter-card {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(15, 23, 42, 0.06);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(14, 124, 123, 0.05);
    }
    .result-caption {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.5rem;
        padding: 0 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Filter card
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
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
st.markdown("</div>", unsafe_allow_html=True)

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

st.markdown(
    f'<div class="result-caption">Menampilkan {len(filtered)} dari {len(df)} total responden.</div>',
    unsafe_allow_html=True,
)

# Column setup (after filtered is available)
question_cols = [q for q in QUESTIONS if q in filtered.columns]
display_cols = [
    "respondent_code", "created_at", "nama_pasien", "umur_display", "jenis_kelamin",
    "lama_dirawat", *question_cols, "saran",
]
display_cols = [c for c in display_cols if c in filtered.columns]

# Table card
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.dataframe(
    filtered.sort_values("created_at", ascending=False)[display_cols].reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
    height=620,
    column_config={
        "created_at": st.column_config.DatetimeColumn("Waktu", format="D MMM YYYY, HH:mm", width="medium"),
        "respondent_code": st.column_config.TextColumn("Kode", width="small"),
        "nama_pasien": st.column_config.TextColumn("Nama", width="large"),
        "umur_display": st.column_config.TextColumn("Umur", width="small"),
        "jenis_kelamin": st.column_config.TextColumn("Jenis Kelamin", width="medium"),
        "lama_dirawat": st.column_config.TextColumn("Lama Dirawat", width="medium"),
        "saran": st.column_config.TextColumn("Saran/Kritik", width="large", max_chars=200),
    },
)
st.markdown("</div>", unsafe_allow_html=True)

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
