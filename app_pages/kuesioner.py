"""Halaman kuesioner — form utama yang diisi oleh pasien/orang tua/wali."""

import base64
from pathlib import Path

import streamlit as st

import database
from utils import (
    CATEGORIES,
    JENIS_KELAMIN_OPTIONS,
    LAMA_DIRAWAT_OPTIONS,
    LIKERT_LABELS,
    QUESTIONS,
    generate_respondent_code,
)

LOGO_PATH = Path(__file__).resolve().parent.parent / "images__1_-removebg-preview.png"
LOGO_DATA_URI = (
    "data:image/png;base64,"
    + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
)

st.markdown(
    """
    <style>
    .kuesioner-header {
        background: linear-gradient(135deg, #0E7C7B 0%, #14A098 100%);
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 14px 28px rgba(14, 124, 123, 0.22);
        border: 1px solid rgba(255,255,255,0.12);
    }
    .kuesioner-header h1 {
        font-size: 1.5rem;
        margin: 0 0 0.35rem 0;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .kuesioner-header p {
        margin: 0;
        opacity: 0.92;
        font-size: 0.93rem;
        line-height: 1.55;
    }
    .home-watermark {
        position: relative;
        display: flex;
        justify-content: center;
        height: 180px;
        margin: 0.25rem 0 0.5rem;
        pointer-events: none;
        overflow: hidden;
    }
    .home-watermark img {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: min(480px, 90vw);
        height: 480px;
        object-fit: contain;
        opacity: 0.4;
        filter: grayscale(15%);
    }
    .category-header {
        display: flex; align-items: center; gap: 0.5rem;
        margin: 1.3rem 0 0.35rem 0;
        font-weight: 800; color: #0E7C7B; font-size: 1.04rem;
        letter-spacing: -0.02em;
    }
    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(14, 124, 123, 0.08);
        border-radius: 22px;
        padding: 1rem 0.9rem 0.4rem;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
    }
    div[data-testid="stRadio"] {
        background: rgba(248, 252, 251, 0.9);
        border: 1px solid rgba(14, 124, 123, 0.08);
        border-radius: 16px;
        padding: 0.45rem 0.55rem 0.15rem;
    }
    [data-baseweb="radio-group"] > label {
        border-radius: 12px;
        padding: 0.35rem 0.5rem;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        border-radius: 14px;
        font-weight: 800;
        padding: 0.9rem 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="home-watermark">
        <img src="{LOGO_DATA_URI}" alt="Watermark RSUD SLG Kediri" />
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="kuesioner-header">
        <h1>📋 Kuesioner Kepuasan Pasien</h1>
        <p>Ruang Anak Rawat Inap Parkit — RSUD SLG Kediri. Jawaban Anda membantu
        kami meningkatkan kualitas pelayanan.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("kuesioner_form", border=False):
    st.markdown("#### :material/badge: Data Responden")
    c1, c2 = st.columns(2)
    with c1:
        nama_pasien = st.text_input(
            "Nama Pasien (opsional)", placeholder="Contoh: Budi"
        )
        umur = st.text_input(
            "Umur Pasien ", placeholder="Masukkan umur",
        )
    with c2:
        jenis_kelamin = st.selectbox(
            "Jenis Kelamin", options=JENIS_KELAMIN_OPTIONS, index=None,
            placeholder="Pilih jenis kelamin",
        )
        lama_dirawat = st.selectbox(
            "Lama Dirawat", options=LAMA_DIRAWAT_OPTIONS, index=None,
            placeholder="Pilih lama perawatan",
        )

    st.divider()
    st.markdown("#### :material/rate_review: Penilaian Pelayanan")
    st.caption("Berikan penilaian Anda untuk setiap pernyataan berikut (1 = Tidak Puas, 5 = Sangat Puas).")

    answers: dict[str, int] = {}
    for category, qkeys in CATEGORIES.items():
        st.markdown(
            f'<div class="category-header">{category}</div>',
            unsafe_allow_html=True,
        )
        for qkey in qkeys:
            answers[qkey] = st.radio(
                QUESTIONS[qkey],
                options=[1, 2, 3, 4, 5],
                format_func=lambda v: f"{v} — {LIKERT_LABELS[v]}",
                horizontal=True,
                index=None,
                key=f"radio_{qkey}",
            )

    st.divider()
    st.markdown("#### :material/chat: Saran & Kritik (opsional)")
    saran = st.text_area(
        "Tulis saran, kritik, atau masukan Anda untuk kami",
        placeholder="Contoh: Pelayanan sudah baik, semoga waktu tunggu makan bisa lebih tepat waktu.",
        height=100,
    )

    st.markdown("")
    submitted = st.form_submit_button(
        "Kirim Kuesioner", type="primary", icon=":material/send:", use_container_width=True
    )

if submitted:
    missing = []
    if not umur.strip():
        missing.append("Umur Pasien")
    if not jenis_kelamin:
        missing.append("Jenis Kelamin")
    if not lama_dirawat:
        missing.append("Lama Dirawat")
    unanswered = [QUESTIONS[k] for k, v in answers.items() if v is None]

    if missing or unanswered:
        st.error(
            "Mohon lengkapi data berikut sebelum mengirim:\n\n"
            + "\n".join(f"- {m}" for m in missing)
            + ("\n" if missing and unanswered else "")
            + "\n".join(f"- {q}" for q in unanswered)
        )
    else:
        payload = {
            "respondent_code": generate_respondent_code(),
            "nama_pasien": nama_pasien.strip() if nama_pasien else None,
            "umur": int(umur) if umur.strip().isdigit() else 0,
            "jenis_kelamin": jenis_kelamin,
            "lama_dirawat": lama_dirawat,
            "saran": saran.strip() if saran else None,
            **answers,
        }
        try:
            with st.spinner("Menyimpan jawaban Anda..."):
                saved = database.insert_response(payload)
            st.session_state["last_response"] = saved or payload
            st.session_state["kuesioner_success"] = True
            st.switch_page("app_pages/terima_kasih.py")
        except database.DatabaseConfigError as exc:
            st.error(
                f":material/error: Aplikasi belum terhubung ke database.\n\n{exc}"
            )
        except RuntimeError as exc:
            st.error(f":material/error: {exc}")
            with st.expander("Detail teknis"):
                st.code(str(exc))
