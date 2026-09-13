"""Ekspor data responden ke CSV atau Excel."""

import io

import pandas as pd
import streamlit as st

import auth
import database
from utils import JENIS_KELAMIN_OPTIONS, LAMA_DIRAWAT_OPTIONS, format_umur

auth.require_admin()

st.markdown("## :material/download: Export Data")
st.caption("Unduh data responden sesuai filter yang dipilih.")

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
df["umur_display"] = df.apply(lambda r: format_umur(r["umur"], r.get("umur_satuan", "tahun")), axis=1)

c1, c2, c3 = st.columns(3)
with c1:
    min_date = df["created_at"].min()
    max_date = df["created_at"].max()
    date_range = st.date_input(
        "Rentang Tanggal",
        value=(min_date.date(), max_date.date()) if pd.notna(min_date) else None,
    )
with c2:
    jk_filter = st.multiselect("Jenis Kelamin", options=JENIS_KELAMIN_OPTIONS)
with c3:
    lama_filter = st.multiselect("Lama Dirawat", options=LAMA_DIRAWAT_OPTIONS)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["created_at"].dt.date >= start) & (filtered["created_at"].dt.date <= end)
    ]
if jk_filter:
    filtered = filtered[filtered["jenis_kelamin"].isin(jk_filter)]
if lama_filter:
    filtered = filtered[filtered["lama_dirawat"].isin(lama_filter)]

export_df = filtered.copy()
if "umur_satuan" in export_df.columns:
    export_df = export_df.drop(columns=["umur_satuan"])
if "umur" in export_df.columns:
    export_df["Umur"] = export_df["umur"].fillna(0).astype(int).astype(str)
    export_df = export_df.drop(columns=["umur"])

st.caption(f"{len(filtered)} baris siap diunduh (dari total {len(df)}).")
st.dataframe(export_df, use_container_width=True, hide_index=True, height=280)

col1, col2 = st.columns(2)
with col1:
    csv_bytes = export_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Download CSV",
        data=csv_bytes,
        file_name="data_responden.csv",
        mime="text/csv",
        icon=":material/description:",
        use_container_width=True,
        disabled=filtered.empty,
    )
with col2:
    try:
        excel_df = export_df.copy()
        if "created_at" in excel_df.columns:
            excel_df["created_at"] = excel_df["created_at"].dt.tz_localize(None)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            excel_df.to_excel(writer, index=False, sheet_name="Responden")
        excel_bytes = buffer.getvalue()
        st.download_button(
            "Download Excel",
            data=excel_bytes,
            file_name="data_responden.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            icon=":material/table_chart:",
            use_container_width=True,
            disabled=filtered.empty,
        )
    except ImportError:
        st.error(
            ":material/error: Modul `openpyxl` belum terinstall. "
            "Jalankan `pip install openpyxl` lalu muat ulang halaman."
        )
    except (OSError, ValueError) as exc:
        st.error(f":material/error: Gagal membuat file Excel: {exc}")
