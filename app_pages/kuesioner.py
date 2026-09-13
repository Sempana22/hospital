"""Halaman kuesioner — form utama yang diisi oleh pasien/orang tua/wali."""

import base64
import re
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

SATUAN_UMUR_OPTIONS = ["Tahun", "Bulan"]

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
    div[data-testid="stTextInput"] > label,
    div[data-testid="stSelectbox"] > label,
    div[data-testid="stDateInput"] > label {
        font-weight: 700;
        color: #0F172A;
    }
    div[data-testid="stTextInput"] > div,
    div[data-testid="stSelectbox"] > div {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(14, 124, 123, 0.18);
        border-radius: 14px;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] select,
    div[data-testid="stTextArea"] textarea {
        border-radius: 14px !important;
        background: rgba(255, 255, 255, 0.96) !important;
        color: #0F172A !important;
        font-weight: 500;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stSelectbox"] select:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: rgba(14, 124, 123, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(20, 160, 152, 0.16) !important;
    }
    div[data-testid="stTextArea"] > div {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(14, 124, 123, 0.18);
        border-radius: 16px;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        border-radius: 14px;
        font-weight: 800;
        padding: 0.9rem 1.2rem;
        background: linear-gradient(135deg, #0E7C7B 0%, #14A098 100%);
        border: none;
        box-shadow: 0 12px 20px rgba(14, 124, 123, 0.22);
    }
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        max-width: 420px;
        display: block;
        margin: 0.75rem auto 0.25rem auto;
    }

    @media (max-width: 640px) {
        .kuesioner-header {
            padding: 1.2rem 1rem;
            border-radius: 16px;
        }
        .kuesioner-header h1 {
            font-size: 1.25rem;
        }
        .kuesioner-header p {
            font-size: 0.82rem;
        }
        .home-watermark {
            height: 120px;
            margin: 0 0 0.25rem;
        }
        .home-watermark img {
            width: min(260px, 76vw);
            height: 260px;
            opacity: 0.22;
        }
        div[data-testid="stForm"] {
            padding: 0.8rem 0.65rem 0.25rem;
            border-radius: 18px;
        }
        [data-baseweb="radio-group"] > label {
            padding: 0.45rem 0.4rem;
        }
        div[data-testid="stButton"] > button[kind="primary"] {
            width: 100%;
            border-radius: 12px;
            padding: 0.85rem 1rem;
        }
        [data-testid="stHorizontalBlock"] {
            gap: 0.25rem !important;
        }
        [data-testid="stRadio"] > div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: 0.5rem;
        }
        div[data-testid="stFormSubmitButton"] > button {
            max-width: 100%;
        }
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
            "Nama Pasien", placeholder="Contoh: Budi"
        )
    with c2:
        jenis_kelamin = st.selectbox(
            "Jenis Kelamin", options=JENIS_KELAMIN_OPTIONS, index=None,
            placeholder="Pilih jenis kelamin",
        )

    c3, c4, c5 = st.columns([1.5, 0.8, 1.5])
    with c3:
        umur_input = st.text_input(
            "Umur Pasien", placeholder="Contoh: 2"
        )
    with c4:
        satuan_umur = st.selectbox(
            "Satuan",
            options=SATUAN_UMUR_OPTIONS,
            index=0,
            help="Pilih satuan umur pasien",
        )
    with c5:
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
    umur_value = None
    umur_satuan_value = "tahun"
    if umur_input is None or not str(umur_input).strip():
        missing.append("Umur Pasien")
    else:
        raw = str(umur_input).strip()
        normalized = raw.lower()

        year_match = re.search(r'(\d+)\s*(tahun|thn)', normalized)
        month_match = re.search(r'(\d+)\s*(bulan|bln)', normalized)

        if year_match and month_match:
            total_months = int(year_match.group(1)) * 12 + int(month_match.group(1))
            umur_value = total_months
            umur_satuan_value = "bulan"
        elif year_match:
            umur_value = int(year_match.group(1))
            umur_satuan_value = "tahun"
        elif month_match:
            umur_value = int(month_match.group(1))
            umur_satuan_value = "bulan"
        else:
            try:
                umur_value = int(raw)
                umur_satuan_value = "tahun" if satuan_umur == "Tahun" else "bulan"
            except ValueError:
                st.error("Umur Pasien harus berupa angka bulat, misalnya 2, 18, 2 bulan, atau 1 tahun 2 bulan.")
                st.stop()

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
            "umur": int(umur_value),
            "umur_satuan": umur_satuan_value,
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
