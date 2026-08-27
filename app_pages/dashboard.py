"""Dashboard admin — ringkasan KPI, filter, dan grafik overview."""

import pandas as pd
import plotly.express as px
import streamlit as st

import auth
import database
from utils import (
    CATEGORIES,
    CATEGORY_COLORS,
    CHART_COLORS,
    JENIS_KELAMIN_OPTIONS,
    LAMA_DIRAWAT_OPTIONS,
    QUESTIONS,
    interpret_score,
    umur_group,
)

auth.require_admin()

st.markdown("## :material/dashboard: Dashboard")
st.caption("Ringkasan tingkat kepuasan pasien Ruang Anak Rawat Inap Parkit.")

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
df["kelompok_umur"] = df["umur"].apply(umur_group)
question_cols = [q for q in QUESTIONS if q in df.columns]
df["skor_keseluruhan"] = df[question_cols].mean(axis=1)

# ─── Filters ────────────────────────────────────────────────────────
with st.expander(":material/filter_alt: Filter Data", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
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
    with c4:
        umur_filter = st.multiselect(
            "Kelompok Umur", options=sorted(df["kelompok_umur"].unique())
        )

filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["created_at"].dt.date >= start) & (filtered["created_at"].dt.date <= end)
    ]
if jk_filter:
    filtered = filtered[filtered["jenis_kelamin"].isin(jk_filter)]
if lama_filter:
    filtered = filtered[filtered["lama_dirawat"].isin(lama_filter)]
if umur_filter:
    filtered = filtered[filtered["kelompok_umur"].isin(umur_filter)]

if filtered.empty:
    st.warning(":material/warning: Tidak ada data yang cocok dengan filter yang dipilih.")
    st.stop()

# ─── KPI cards ──────────────────────────────────────────────────────
category_avgs = {}
for category, qkeys in CATEGORIES.items():
    cols_present = [q for q in qkeys if q in filtered.columns]
    if cols_present:
        category_avgs[category] = filtered[cols_present].mean(axis=1).mean()

overall_avg = filtered["skor_keseluruhan"].mean()
top_category = max(category_avgs, key=category_avgs.get) if category_avgs else "-"
low_category = min(category_avgs, key=category_avgs.get) if category_avgs else "-"

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Responden", len(filtered))
k2.metric("Rata-rata Kepuasan", f"{overall_avg:.2f} / 5", interpret_score(overall_avg))
k3.metric("Kategori Tertinggi", top_category, f"{category_avgs.get(top_category, 0):.2f}")
k4.metric("Kategori Terendah", low_category, f"{category_avgs.get(low_category, 0):.2f}")

st.divider()

# ─── Charts ─────────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    st.markdown("##### Rata-rata Skor per Kategori")
    cat_df = pd.DataFrame(
        {"Kategori": list(category_avgs.keys()), "Rata-rata": list(category_avgs.values())}
    )
    fig = px.bar(
        cat_df, x="Rata-rata", y="Kategori", orientation="h", range_x=[0, 5],
        color="Kategori", color_discrete_sequence=CATEGORY_COLORS, text_auto=".2f",
    )
    fig.update_layout(showlegend=False, height=320, margin=dict(l=0, r=10, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("##### Distribusi Kepuasan Keseluruhan")
    dist = filtered["skor_keseluruhan"].apply(interpret_score).value_counts().reset_index()
    dist.columns = ["Interpretasi", "Jumlah"]
    fig2 = px.pie(
        dist, names="Interpretasi", values="Jumlah", hole=0.5,
        color_discrete_sequence=list(CHART_COLORS.values()),
    )
    fig2.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("##### Rata-rata per Pertanyaan")
q_avgs = filtered[question_cols].mean().sort_values()
q_df = pd.DataFrame(
    {"Pertanyaan": [QUESTIONS[q][:45] + "…" if len(QUESTIONS[q]) > 45 else QUESTIONS[q] for q in q_avgs.index],
     "Rata-rata": q_avgs.values}
)
fig3 = px.bar(q_df, x="Rata-rata", y="Pertanyaan", orientation="h", range_x=[0, 5], text_auto=".2f")
fig3.update_traces(marker_color=CHART_COLORS["primary"])
fig3.update_layout(height=420, margin=dict(l=0, r=10, t=10, b=0))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("##### Data Responden Terbaru")
show_cols = ["respondent_code", "created_at", "nama_pasien", "umur", "jenis_kelamin", "lama_dirawat", "skor_keseluruhan"]
show_cols = [c for c in show_cols if c in filtered.columns]
st.dataframe(
    filtered.sort_values("created_at", ascending=False)[show_cols].head(10),
    use_container_width=True, hide_index=True,
)
