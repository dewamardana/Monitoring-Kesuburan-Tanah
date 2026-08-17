# 🌱 Monitoring Kesuburan Tanah — Dashboard Web (Flask + Supabase + ML)

Dashboard web real-time untuk memantau kesuburan tanah, menggabungkan **Flask**, database cloud **Supabase**, dan model **machine learning** untuk prediksi otomatis.

## 📌 Deskripsi & Arsitektur (berdasarkan isi kode `app.py`)

Sistem ini menerima data sensor tanah (pH, suhu, kelembapan) yang dikirim oleh perangkat ESP32/Arduino (lihat [`Monitoring-Kesuburan-Tanah-Kode-Alat`](https://github.com/dewamardana/Monitoring-Kesuburan-Tanah-Kode-Alat)), menyimpannya ke database cloud **Supabase**, lalu memproses data tersebut melalui model machine learning terlatih untuk memprediksi tingkat kesuburan tanah.

```
Perangkat ESP32 (sensor pH, suhu, kelembapan)
   → kirim data → Supabase (tabel `data`, per id_micro — mendukung banyak perangkat sekaligus)
   → Flask ambil data terbaru → diproses dengan Pandas → discale (scaler.sav)
   → diprediksi (trained_model.sav) → hasil disimpan ke Supabase (tabel `Hasil`)
   → ditampilkan sebagai grafik (chart1.html, chart2.html)
```

## ✨ Fitur Utama

- 🔑 **Login berbasis Supabase** — autentikasi pengguna disimpan & divalidasi lewat tabel `user` di Supabase
- 📡 **Multi-Perangkat** — data diidentifikasi per `id_micro`, memungkinkan sistem memantau lebih dari satu perangkat sensor sekaligus
- 🤖 **Prediksi Otomatis** — begitu data baru diambil, sistem otomatis men-scale dan memprediksi kesuburan tanah menggunakan model scikit-learn yang sudah dilatih sebelumnya
- 📈 **Visualisasi Grafik** — beberapa halaman chart (`/chart/<micro>`, `/chart1/<micro>`, `/2`) untuk menampilkan tren data per perangkat
- 🔍 **Endpoint Test Koneksi** — `/test-connection` untuk memverifikasi koneksi ke Supabase

## ⚙️ Teknologi

- **Backend:** Python, Flask
- **Database:** Supabase (Postgres as a Service)
- **Machine Learning:** scikit-learn (model & scaler disimpan dalam format pickle `.sav`), Pandas, NumPy
- **Deployment:** Vercel (`vercel.json` tersedia)

## 🚀 Cara Menjalankan

```bash
git clone https://github.com/dewamardana/Monitoring-Kesuburan-Tanah.git
cd Monitoring-Kesuburan-Tanah
pip install -r requirements.txt
python app.py
```
Akses di `http://localhost:5000`.

## 🔗 Riwayat Project — Bagian dari Rangkaian yang Sama

1. **(repo ini)** — dashboard web + model ML (versi awal)
2. [`Monitoring-Kesuburan-Tanah-Kode-Alat`](https://github.com/dewamardana/Monitoring-Kesuburan-Tanah-Kode-Alat) — firmware Arduino pasangan repo ini
3. [`Monitoring-soil-contamination-by-implementing-fuzzy-logic`](https://github.com/dewamardana/Monitoring-soil-contamination-by-implementing-fuzzy-logic) — versi upgrade dengan logika fuzzy
