"""Statistik deskriptif dan grafik tren."""

import pandas as pd
import plotly.express as px
import streamlit as st

import auth
import database
from utils import CATEGORIES, CHART_COLORS, LIKERT_COLORS, LIKERT_LABELS, QUESTIONS, interpret_score

auth.require_admin()

st.markdown(
    """
    <style>
    .admin-page-header {
        background: linear-gradient(135deg, rgba(10,77,76,0.96), rgba(15,113,109,0.94), rgba(20,160,152,0.9));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 26px;
        padding: 1.25rem 1.4rem 1.1rem;
        margin-bottom: 1rem;
        color: white;
        box-shadow: 0 18px 36px rgba(14,124,123,0.16);
    }
    .admin-page-header h2 {
        margin: 0;
        font-size: clamp(1.4rem, 2.2vw, 1.9rem);
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    .admin-page-header p {
        margin: 0.45rem 0 0;
        color: rgba(255,255,255,0.82);
        font-size: 0.82rem;
        font-weight: 600;
    }
    .analytic-shell {
        background: rgba(255,255,255,0.68);
        border: 1px solid rgba(14,124,123,0.08);
        border-radius: 20px;
        padding: 0.9rem;
        margin-bottom: 1rem;
        box-shadow: 0 12px 26px rgba(15,23,42,0.04);
    }
    div[data-testid="stPlotlyChart"] > div {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 15px 28px rgba(15,23,42,0.05);
        border: 1px solid rgba(14,124,123,0.08);
    }
    .stTabs [role="tablist"] {
        gap: 0.5rem;
    }
    .stTabs [role="tablist"] button {
        border-radius: 12px 12px 0 0;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="admin-page-header">
        <h2>📊 Statistik</h2>
        <p>Analisis deskriptif dan tren kepuasan pasien dari waktu ke waktu.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
question_cols = [q for q in QUESTIONS if q in df.columns]
df["skor_keseluruhan"] = df[question_cols].mean(axis=1)

st.markdown('<div class="analytic-shell">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Tren Waktu", "Distribusi Jawaban", "Statistik Deskriptif"])

with tab1:
    st.markdown("##### Tren Rata-rata Kepuasan Harian")
    daily = (
        df.set_index("created_at")["skor_keseluruhan"]
        .resample("D").mean().dropna().reset_index()
    )
    if len(daily) >= 2:
        fig = px.line(daily, x="created_at", y="skor_keseluruhan", markers=True, range_y=[1, 5])
        fig.update_traces(
            line_color=CHART_COLORS["primary"],
            line_width=3,
            marker_size=7,
            hovertemplate='<b>%{x}</b><br>Rata-rata: %{y:.2f}<extra></extra>',
        )
        fig.update_layout(
            height=380,
            xaxis_title="Tanggal",
            yaxis_title="Rata-rata Skor",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            transition_duration=500,
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    else:
        st.info("Data belum cukup untuk menampilkan tren (perlu lebih dari satu hari data).")

with tab2:
    st.markdown("##### Distribusi Jawaban per Pertanyaan")
    qkey = st.selectbox("Pilih Pertanyaan", options=question_cols, format_func=lambda q: f"{q.upper()} — {QUESTIONS[q]}")
    counts = df[qkey].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).reset_index()
    counts.columns = ["Skor", "Jumlah"]
    counts["Label"] = counts["Skor"].map(LIKERT_LABELS)
    fig = px.bar(
        counts, x="Label", y="Jumlah", text_auto=True,
        color="Skor", color_discrete_map={k: v for k, v in LIKERT_COLORS.items()},
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>',
        marker_line_width=0,
    )
    fig.update_layout(
        showlegend=False,
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        transition_duration=500,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})

with tab3:
    st.markdown("##### Statistik Deskriptif per Kategori")
    rows = []
    for category, qkeys in CATEGORIES.items():
        cols_present = [q for q in qkeys if q in df.columns]
        if not cols_present:
            continue
        scores = df[cols_present].mean(axis=1)
        rows.append({
            "Kategori": category,
            "Rata-rata": round(scores.mean(), 2),
            "Median": round(scores.median(), 2),
            "Std. Deviasi": round(scores.std(), 2),
            "Min": round(scores.min(), 2),
            "Max": round(scores.max(), 2),
            "Interpretasi": interpret_score(scores.mean()),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("##### Statistik per Pertanyaan")
    q_rows = []
    for q in question_cols:
        s = df[q]
        q_rows.append({
            "Kode": q.upper(),
            "Pertanyaan": QUESTIONS[q],
            "Rata-rata": round(s.mean(), 2),
            "Std. Deviasi": round(s.std(), 2),
            "Interpretasi": interpret_score(s.mean()),
        })
    st.dataframe(pd.DataFrame(q_rows), use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)
