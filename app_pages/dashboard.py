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
    format_umur,
    interpret_score,
    umur_group,
)

auth.require_admin()

st.markdown(
    """
    <style>
    .dashboard-hero {
        background: linear-gradient(135deg, rgba(10,77,76,0.96), rgba(15,113,109,0.94), rgba(20,160,152,0.9));
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 28px;
        padding: 1.45rem 1.55rem 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 24px 48px rgba(14,124,123,0.17);
        position: relative;
        overflow: hidden;
        animation: dashboardRise 0.45s ease-out;
    }
    .dashboard-hero::after {
        content: "";
        position: absolute;
        inset: auto -20% -35% auto;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(255,255,255,0.18), transparent 70%);
        border-radius: 50%;
    }
    .dashboard-brand {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        position: relative;
        z-index: 1;
    }
    .dashboard-badge {
        width: 56px;
        height: 56px;
        border-radius: 18px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.45rem;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.15);
    }
    .dashboard-brand h1 {
        margin: 0;
        color: white;
        font-size: clamp(1.3rem, 2.2vw, 2.1rem);
        line-height: 1.18;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    .dashboard-brand span {
        display: block;
        color: rgba(255,255,255,0.8);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }
    .dashboard-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 0.92rem;
        position: relative;
        z-index: 1;
    }
    .dashboard-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.46rem 0.78rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.15);
        background: rgba(255,255,255,0.08);
        color: #eafdfb;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .executive-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
        margin: 1rem 0 1.5rem;
    }
    .executive-card {
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(14,124,123,0.08);
        border-radius: 20px;
        padding: 1.05rem 1rem 0.85rem;
        box-shadow: 0 16px 30px rgba(15,23,42,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        min-height: 120px;
    }
    .executive-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 32px rgba(15,23,42,0.08);
    }
    .executive-label {
        color: #5f6e88;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .executive-value {
        color: #101828;
        font-size: clamp(1.3rem, 2vw, 2rem);
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.35rem;
    }
    .executive-meta {
        color: #0e7c7b;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .dashboard-shell {
        animation: dashboardRise 0.5s ease-out;
    }
    @keyframes dashboardRise {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    div[data-testid="stPlotlyChart"] > div {
        border-radius: 22px !important;
        overflow: hidden;
        box-shadow: 0 18px 32px rgba(15, 23, 42, 0.06);
        border: 1px solid rgba(14,124,123,0.08);
        background: rgba(255,255,255,0.7);
    }
    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(14,124,123,0.08);
        box-shadow: 0 14px 28px rgba(15,23,42,0.04);
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(14,124,123,0.08);
        border-radius: 16px;
        box-shadow: 0 10px 20px rgba(15,23,42,0.03);
        background: rgba(255,255,255,0.64);
    }
    @media (max-width: 900px) {
        .executive-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    @media (max-width: 640px) {
        .dashboard-hero {
            padding: 1rem 1rem 0.9rem;
            border-radius: 20px;
        }
        .dashboard-brand {
            align-items: flex-start;
        }
        .dashboard-meta {
            gap: 0.45rem;
        }
        .executive-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="dashboard-hero">
        <div class="dashboard-brand">
            <div class="dashboard-badge">📊</div>
            <div>
                <span>RSUD SLG Kediri</span>
                <h1>Dashboard Admin</h1>
            </div>
        </div>
        <div class="dashboard-meta">
            <div class="dashboard-pill">📈 Executive Summary</div>
            <div class="dashboard-pill">🕒 Live Monitoring</div>
            <div class="dashboard-pill">🏥 Ruang Anak Rawat Inap Parkit</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Ringkasan kinerja layanan pasien dalam satu tampilan pengelolaan yang terarah.")

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

summary_cards = [
    ("Total Responden", str(len(filtered)), "Volume data aktif"),
    ("Index Kepuasan", f"{overall_avg:.2f} / 5", interpret_score(overall_avg)),
    ("Kategori Tertinggi", top_category, f"Skor {category_avgs.get(top_category, 0):.2f}"),
    ("Kategori Terendah", low_category, f"Skor {category_avgs.get(low_category, 0):.2f}"),
]

st.markdown(
    """
    <div class="executive-grid">
        <div class="executive-card">
            <div class="executive-label">Total Responden</div>
            <div class="executive-value">{}</div>
            <div class="executive-meta">Volume data aktif</div>
        </div>
        <div class="executive-card">
            <div class="executive-label">Index Kepuasan</div>
            <div class="executive-value">{:.2f} / 5</div>
            <div class="executive-meta">{}</div>
        </div>
        <div class="executive-card">
            <div class="executive-label">Kategori Tertinggi</div>
            <div class="executive-value">{}</div>
            <div class="executive-meta">Skor {:.2f}</div>
        </div>
        <div class="executive-card">
            <div class="executive-label">Kategori Terendah</div>
            <div class="executive-value">{}</div>
            <div class="executive-meta">Skor {:.2f}</div>
        </div>
    </div>
    """.format(
        len(filtered),
        overall_avg,
        interpret_score(overall_avg),
        top_category,
        category_avgs.get(top_category, 0),
        low_category,
        category_avgs.get(low_category, 0),
    ),
    unsafe_allow_html=True,
)

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
    fig.update_traces(marker_line_width=0, opacity=0.96, hovertemplate='<b>%{y}</b><br>Rata-rata: %{x:.2f}<extra></extra>')
    fig.update_layout(
        showlegend=False,
        height=320,
        margin=dict(l=0, r=10, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        transition_duration=500,
        hovermode="y unified",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})

with c2:
    st.markdown("##### Distribusi Kepuasan Keseluruhan")
    dist = filtered["skor_keseluruhan"].apply(interpret_score).value_counts().reset_index()
    dist.columns = ["Interpretasi", "Jumlah"]
    fig2 = px.pie(
        dist, names="Interpretasi", values="Jumlah", hole=0.5,
        color_discrete_sequence=list(CHART_COLORS.values()),
    )
    fig2.update_traces(textinfo="percent+label", hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<extra></extra>', marker_line_width=0)
    fig2.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        transition_duration=500,
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False, "responsive": True})

st.markdown("##### Rata-rata per Pertanyaan")
q_avgs = filtered[question_cols].mean().sort_values()
q_df = pd.DataFrame(
    {"Pertanyaan": [QUESTIONS[q][:45] + "…" if len(QUESTIONS[q]) > 45 else QUESTIONS[q] for q in q_avgs.index],
     "Rata-rata": q_avgs.values}
)
fig3 = px.bar(q_df, x="Rata-rata", y="Pertanyaan", orientation="h", range_x=[0, 5], text_auto=".2f")
fig3.update_traces(
    marker_color=CHART_COLORS["primary"],
    marker_line_width=0,
    hovertemplate='<b>%{y}</b><br>Rata-rata: %{x:.2f}<extra></extra>',
)
fig3.update_layout(
    height=420,
    margin=dict(l=0, r=10, t=10, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    transition_duration=500,
    hovermode="y unified",
)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False, "responsive": True})

filtered["umur_display"] = filtered.apply(lambda r: format_umur(r["umur"], r.get("umur_satuan", "tahun")), axis=1)
st.markdown("##### Data Responden Terbaru")
show_cols = ["respondent_code", "created_at", "nama_pasien", "umur_display", "jenis_kelamin", "lama_dirawat", "skor_keseluruhan"]
show_cols = [c for c in show_cols if c in filtered.columns]
st.dataframe(
    filtered.sort_values("created_at", ascending=False)[show_cols].head(10),
    use_container_width=True, hide_index=True,
)
