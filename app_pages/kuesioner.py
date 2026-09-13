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
        border-radius: 18px;
        padding: 1.75rem 1.5rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 24px rgba(14, 124, 123, 0.25);
    }
    .kuesioner-header h1 { font-size: 1.4rem; margin: 0 0 0.3rem 0; font-weight: 800; }
    .kuesioner-header p { margin: 0; opacity: 0.9; font-size: 0.92rem; }
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
        margin: 1.25rem 0 0.25rem 0;
        font-weight: 700; color: #0E7C7B; font-size: 1.02rem;
    }
    .stNumberInput input[type="number"]::-webkit-outer-spin-button,
    .stNumberInput input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    .stNumberInput input[type="number"] {
        -moz-appearance: textfield;
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
        umur_tahun = st.number_input(
            "Umur Pasien (tahun)",
            min_value=0,
            max_value=18,
            step=1,
            value=None,
            format="%d",
            placeholder="Contoh: 1",
            help="Isi umur dalam tahun bila pasien sudah berusia 1 tahun atau lebih.",
        )
        umur_bulan = st.number_input(
            "Umur Pasien (bulan)",
            min_value=0,
            max_value=11,
            step=1,
            value=None,
            format="%d",
            placeholder="Contoh: 6 untuk 6 bulan",
            help="Isi umur dalam bulan bila pasien masih di bawah 1 tahun.",
        )
        umur = None
        if umur_tahun is not None or umur_bulan is not None:
            tahun = umur_tahun or 0
            bulan = umur_bulan or 0
            umur = tahun + (bulan / 12.0)
            if umur > 18:
                st.error("Umur maksimal 18 tahun.")
                umur = None
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
    if umur is None:
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
            "umur": float(umur),
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
