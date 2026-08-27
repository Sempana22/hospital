"""Halaman konfirmasi setelah kuesioner berhasil dikirim."""

import streamlit as st

from utils import CATEGORIES, QUESTIONS, interpret_score

st.markdown(
    """
    <style>
    .thanks-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1px solid #A7F3D0;
        border-radius: 18px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .thanks-card h1 { color: #065F46; font-size: 1.6rem; margin: 0.5rem 0; }
    .thanks-card p { color: #047857; margin: 0; }
    .code-chip {
        display: inline-block; margin-top: 0.75rem;
        background: white; border: 1px dashed #10B981;
        border-radius: 10px; padding: 0.4rem 1rem;
        font-family: monospace; font-weight: 700; color: #065F46;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

last_response = st.session_state.get("last_response")

if not last_response:
    st.info(
        "Belum ada kuesioner yang dikirim pada sesi ini. Silakan isi kuesioner terlebih dahulu."
    )
    if st.button("Isi Kuesioner", type="primary", icon=":material/assignment:"):
        st.switch_page("app_pages/kuesioner.py")
    st.stop()

code = last_response.get("respondent_code", "-")

st.markdown(
    f"""
    <div class="thanks-card">
        <div style="font-size:3rem;">🎉</div>
        <h1>Terima Kasih!</h1>
        <p>Jawaban Anda telah berhasil kami terima dan sangat berarti bagi kami
        untuk terus meningkatkan pelayanan.</p>
        <div class="code-chip">Kode Responden: {code}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### :material/summarize: Ringkasan Jawaban Anda")

rows = []
for category, qkeys in CATEGORIES.items():
    scores = [last_response.get(q) for q in qkeys if last_response.get(q) is not None]
    if scores:
        avg = sum(scores) / len(scores)
        rows.append({"Kategori": category, "Rata-rata": round(avg, 2), "Interpretasi": interpret_score(avg)})

if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)

if last_response.get("saran"):
    st.markdown("#### :material/chat: Saran Anda")
    st.info(last_response["saran"])

st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("Isi Kuesioner Lagi", icon=":material/refresh:", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("radio_q"):
                del st.session_state[key]
        st.session_state.pop("last_response", None)
        st.switch_page("app_pages/kuesioner.py")
