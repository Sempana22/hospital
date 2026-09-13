"""Halaman konfirmasi setelah kuesioner berhasil dikirim."""

import streamlit as st

from utils import CATEGORIES, QUESTIONS, interpret_score

st.markdown(
    """
    <style>
    .thanks-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 24px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.12);
    }
    .thanks-card h1 {
        color: #065F46;
        font-size: clamp(1.5rem, 2.6vw, 2.2rem);
        margin: 0.65rem 0;
        font-weight: 800;
    }
    .thanks-card p {
        color: #047857;
        margin: 0;
        line-height: 1.6;
    }
    .summary-panel {
        background: rgba(255,255,255,0.74);
        border: 1px solid rgba(14, 124, 123, 0.1);
        border-radius: 18px;
        padding: 1rem 1rem 0.25rem;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
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

st.markdown(
    f"""
    <div class="thanks-card">
        <div style="font-size:3rem;">🎉</div>
        <h1>Terima Kasih!</h1>
        <p>Jawaban Anda telah berhasil kami terima dan sangat berarti bagi kami
        untuk terus meningkatkan pelayanan.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### :material/summarize: Ringkasan Jawaban Anda")

st.markdown('<div class="summary-panel">', unsafe_allow_html=True)
rows = []
for category, qkeys in CATEGORIES.items():
    scores = [last_response.get(q) for q in qkeys if last_response.get(q) is not None]
    if scores:
        avg = sum(scores) / len(scores)
        rows.append({"Kategori": category, "Rata-rata": round(avg, 2), "Interpretasi": interpret_score(avg)})

if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

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
