"""Shared utilities and constants for the hospital survey application."""

import random
import string
from datetime import datetime

# ─── Likert scale labels ──────────────────────────────────────────────
LIKERT_LABELS = {
    1: "Tidak Puas",
    2: "Kurang Puas",
    3: "Cukup Puas",
    4: "Puas",
    5: "Sangat Puas",
}

# ─── Questions ─────────────────────────────────────────────────────────
QUESTIONS = {
    "q1": "Kebersihan kamar dan lingkungan di Ruang Anak Rawat Inap Parkit",
    "q2": "Kenyamanan tempat tidur dan fasilitas kamar yang tersedia",
    "q3": "Kebersihan kamar mandi/toilet yang tersedia",
    "q4": "Keramahan dan kesopanan perawat dalam memberikan pelayanan",
    "q5": "Kecepatan perawat dalam merespons kebutuhan atau keluhan pasien",
    "q6": "Penjelasan perawat mengenai kondisi dan perawatan anak selama dirawat",
    "q7": "Sikap dokter dalam memberikan pelayanan dan menjelaskan kondisi pasien",
    "q8": "Kecepatan dan ketepatan pelayanan kesehatan yang diberikan kepada anak",
    "q9": "Keamanan dan ketenangan lingkungan selama anak menjalani rawat inap",
    "q10": "Ketepatan waktu pemberian makanan kepada pasien",
    "q11": "Kepuasan keseluruhan terhadap pelayanan Ruang Anak Rawat Inap Parkit RSUD SLG Kediri",
    "q12": "Seberapa puas Anda terhadap ketepatan waktu pemberian makanan kepada pasien selama dirawat di Ruang Anak Rawat Inap Parkit?",
}

# ─── Category grouping ─────────────────────────────────────────────────
CATEGORIES = {
    "Fasilitas": ["q1", "q2", "q3"],
    "Pelayanan Perawat": ["q4", "q5", "q6"],
    "Pelayanan Medis": ["q7", "q8"],
    "Pelayanan Gizi": ["q10", "q12"],
    "Lingkungan & Keamanan": ["q9"],
    "Kepuasan Keseluruhan": ["q11"],
}

CATEGORY_ICONS = {
    "Fasilitas": ":material/king_bed:",
    "Pelayanan Perawat": ":material/health_and_safety:",
    "Pelayanan Medis": ":material/stethoscope:",
    "Pelayanan Gizi": ":material/restaurant:",
    "Lingkungan & Keamanan": ":material/shield:",
    "Kepuasan Keseluruhan": ":material/favorite:",
}

# ─── Form option constants (shared so filters everywhere match exactly) ──
JENIS_KELAMIN_OPTIONS = ["Laki-laki", "Perempuan"]
LAMA_DIRAWAT_OPTIONS = ["1-3 hari", "4-7 hari", "> 7 hari"]


# ─── Satisfaction interpretation ───────────────────────────────────────
def interpret_score(score: float) -> str:
    """Return interpretation label for a given average score."""
    if score is None:
        return "-"
    if score >= 4.21:
        return "Sangat Puas"
    elif score >= 3.41:
        return "Puas"
    elif score >= 2.61:
        return "Cukup Puas"
    elif score >= 1.81:
        return "Kurang Puas"
    else:
        return "Tidak Puas"


# ─── Colors for charts ────────────────────────────────────────────────
# Brand-inspired teal palette consistent with the sidebar theme
CHART_COLORS = {
    "primary": "#0E7C7B",
    "secondary": "#14A098",
    "tertiary": "#1BC6CF",
    "accent": "#34D399",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}

# Categorical colors for Likert distribution (1-5 scale)
LIKERT_COLORS = {
    1: "#EF4444",   # Red - Tidak Puas
    2: "#F97316",   # Orange - Kurang Puas
    3: "#F59E0B",   # Amber - Cukup Puas
    4: "#22C55E",   # Green - Puas
    5: "#0E7C7B",   # Teal - Sangat Puas
}

# Category colors for bar charts
CATEGORY_COLORS = [
    "#0E7C7B",  # Teal
    "#3B82F6",  # Blue
    "#8B5CF6",  # Purple
    "#F59E0B",  # Amber
    "#EF4444",  # Red
    "#EC4899",  # Pink
]


# ─── Helper functions ──────────────────────────────────────────────────
def generate_respondent_code() -> str:
    """Generate a unique respondent code like R-20260826-A3F1."""
    date_part = datetime.now().strftime("%Y%m%d")
    rand_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"R-{date_part}-{rand_part}"


def umur_group(umur: int) -> str:
    """Bucket a patient's age (in years) into a readable group label."""
    if umur is None:
        return "-"
    if umur < 1:
        return "< 1 tahun"
    if umur <= 5:
        return "1-5 tahun"
    if umur <= 12:
        return "6-12 tahun"
    return "> 12 tahun"
