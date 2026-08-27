# Kuesioner Kepuasan Pasien Ruang Anak Rawat Inap Parkit RSUD SLG Kediri

Aplikasi kuesioner kepuasan pasien berbasis Streamlit dengan database online Supabase PostgreSQL.

## Apa yang diperbaiki di versi ini

1. **Tombol "Masuk" sekarang selalu berfungsi.** Versi sebelumnya menampilkan
   splash screen dengan tombol HTML yang dikendalikan lewat JavaScript lintas
   iframe (`window.parent.document`), yang sering diblokir browser dan
   membuat tombol tidak merespons. Sekarang halaman awal memakai tombol
   Streamlit asli (`st.button`) — begitu diklik, aplikasi langsung
   berpindah ke halaman **Kuesioner** (beranda).
2. **File halaman yang hilang dibuat ulang.** `streamlit_app.py` sudah
   merujuk ke `app_pages/kuesioner.py`, `terima_kasih.py`, `admin_login.py`,
   `dashboard.py`, `data_responden.py`, `statistik.py`, `saran_kritik.py`,
   dan `export_data.py` — namun folder `app_pages/` tidak ada di file yang
   diunggah, sehingga aplikasi akan langsung error saat dijalankan. Semua
   halaman ini sekarang tersedia dan berfungsi penuh.
3. **Pertanyaan `q12` tentang ketepatan waktu pemberian makanan ditambahkan.**
   Pertanyaan ini tersedia sebagai pertanyaan terpisah dari `q10` dan tersimpan
   pada kolom `q12` di database.
4. **Row Level Security (RLS) diperbaiki.** Kebijakan lama hanya mengizinkan
   role `authenticated`/`service_role` untuk `SELECT`, padahal aplikasi
   selalu terhubung dengan **anon key**. Akibatnya, semua halaman admin
   (Dashboard, Data Responden, dst.) akan gagal memuat data meski sudah
   login. Sekarang `anon` juga diizinkan `SELECT` (keamanan akses admin
   tetap dijaga di level aplikasi lewat `auth.require_admin()`).
5. **Penanganan error yang lebih ramah.** Jika `secrets.toml` belum diisi
   atau koneksi Supabase gagal, aplikasi menampilkan pesan yang jelas
   (bahasa Indonesia) alih-alih traceback mentah.
6. **Tampilan diperbarui** — halaman awal, kuesioner, dan seluruh halaman
   admin memakai kartu, warna teal yang konsisten, ikon, dan tata letak yang
   lebih rapi dan mobile-friendly.

## Fitur

### Sisi Responden
- Halaman awal dengan tombol **Masuk** yang membawa langsung ke beranda kuesioner
- Formulir kuesioner dengan skala Likert 1–5, dikelompokkan per kategori
- Data demografi responden (nama, umur, jenis kelamin, lama dirawat)
- Validasi input lengkap sebelum submit
- Penyimpanan data ke database online (Supabase)
- Halaman konfirmasi dengan ringkasan jawaban per kategori

### Sisi Admin
- Login admin dengan autentikasi
- Dashboard KPI dengan filter (tanggal, jenis kelamin, umur, lama dirawat)
- Statistik deskriptif, tren waktu, dan distribusi jawaban
- Tabel data responden dengan pencarian dan filter
- Halaman saran/kritik
- Export data ke CSV dan Excel

---

## 1. Install Dependency

```bash
git clone <repo-url>
cd hospital_survey

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

## 2. Buat Database Supabase

1. Buka [Supabase](https://supabase.com) dan buat akun
2. Klik **"New Project"**, isi nama project, database password, dan region terdekat
3. Tunggu project selesai dibuat

## 3. Buat Tabel

1. Buka **SQL Editor** di dashboard Supabase
2. Paste seluruh isi file `schema.sql`
3. Klik **"Run"**

Tabel `responses` akan dibuat dengan kolom `q1`–`q12`, data demografi, dan `saran`, lengkap dengan Row Level Security.

## 4. Atur Streamlit Secrets

Salin `.streamlit/secrets.toml.example` menjadi `.streamlit/secrets.toml`, lalu isi:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "ganti-password-ini"
```

Ambil `SUPABASE_URL` dan `SUPABASE_KEY` dari **Settings → API** di dashboard Supabase.

**Penting:** Jangan pernah commit `secrets.toml` ke repository (sudah ada di `.gitignore`).

## 5. Jalankan Aplikasi

```bash
streamlit run streamlit_app.py
```

Buka `http://localhost:8501`. Klik **Masuk** untuk memulai kuesioner.

## 6. Deploy ke Streamlit Community Cloud

1. Push kode ke GitHub
2. Buka [Streamlit Community Cloud](https://share.streamlit.io) → **New app**
3. Pilih repository, branch, dan set **Main file path** ke `streamlit_app.py`
4. Di **Advanced settings → Secrets**, paste isi `secrets.toml` Anda
5. Klik **Deploy**

## 7. Login Admin

Username & password sesuai `secrets.toml` (default contoh: `admin` / ganti sendiri).
Login diperlukan untuk mengakses Dashboard, Data Responden, Statistik, Saran & Kritik, dan Export Data.

## 8. Keamanan Data

- **Database:** Row Level Security (RLS) aktif di Supabase
- **API Key:** disimpan di Streamlit Secrets, tidak di source code
- **Password admin:** disimpan di secrets (untuk produksi nyata, gunakan hashing)
- **Identitas:** kode responden digunakan sebagai pengganti nama pasien di dashboard

---

## Struktur Project

```
hospital_survey/
├── streamlit_app.py           # Entry point + halaman awal (welcome/Masuk)
├── database.py                # Koneksi dan query Supabase
├── auth.py                    # Autentikasi admin
├── utils.py                   # Konstanta dan utilitas bersama
├── schema.sql                 # Schema database untuk Supabase
├── requirements.txt           # Python dependencies
├── index.html                 # Landing page statis (opsional)
├── .gitignore
├── README.md
├── .streamlit/
│   ├── config.toml            # Tema aplikasi (teal)
│   └── secrets.toml.example   # Salin jadi secrets.toml lalu isi
└── app_pages/
    ├── kuesioner.py           # Beranda — form kuesioner responden
    ├── terima_kasih.py        # Halaman konfirmasi submit
    ├── admin_login.py         # Login / logout admin
    ├── dashboard.py           # Dashboard admin (KPI + grafik)
    ├── data_responden.py      # Tabel data responden
    ├── statistik.py           # Statistik deskriptif & tren
    ├── saran_kritik.py        # Daftar saran/kritik
    └── export_data.py         # Export CSV/Excel
```

## Teknologi

- **Backend:** Python, Streamlit
- **Database:** Supabase (PostgreSQL)
- **Visualisasi:** Plotly
- **Export:** Pandas, OpenPyXL
- **Tema:** Custom Streamlit theme (teal)

## License

Dibuat untuk kepentingan evaluasi dan peningkatan kualitas pelayanan RSUD SLG Kediri.
