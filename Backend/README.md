# 🤟 BISINDO — Sistem Deteksi Bahasa Isyarat Indonesia

Aplikasi web realtime untuk mendeteksi Bahasa Isyarat Indonesia (BISINDO)
menggunakan webcam browser, Flask backend, MediaPipe, dan Machine Learning.

---

## 📁 Struktur Project

```
project/                        ← Folder utama project kamu
│
├── bisindo_model.pkl            ← Model ML yang sudah di-train
├── dataset_gambar/
├── dataset_tangan.csv
├── collect_dataset.py
├── extract_landmark.py
├── realtime_detection.py
├── train_model.py
│
└── bisindo_web/                 ← Folder web app (ini yang dibuat)
    ├── app.py                   ← Backend Flask
    ├── requirements.txt         ← Library Python
    ├── templates/
    │   └── index.html           ← Halaman utama
    └── static/
        ├── css/
        │   └── style.css        ← Styling UI
        └── js/
            └── script.js        ← Logic frontend
```

---

## ⚙️ Cara Menjalankan

### Langkah 1 — Pastikan Struktur Folder Benar
File `bisindo_model.pkl` harus berada **satu level di atas** folder `bisindo_web/`.

```
project/
├── bisindo_model.pkl   ✅ Di sini
└── bisindo_web/
    └── app.py
```

### Langkah 2 — Install Library Python

Buka terminal, masuk ke folder `bisindo_web/`, lalu jalankan:

```bash
pip install -r requirements.txt
```

### Langkah 3 — Jalankan Server Flask

```bash
cd bisindo_web
python app.py
```

Output yang muncul jika berhasil:
```
==================================================
  🤟 BISINDO Detection System - Server Aktif
==================================================
  URL: http://localhost:5000
  Model: ✅ Loaded
==================================================
```

### Langkah 4 — Buka Browser

Buka browser (Chrome/Firefox) dan akses:

```
http://localhost:5000
```

### Langkah 5 — Mulai Deteksi

1. Klik tombol **"Mulai Kamera"**
2. Izinkan akses kamera saat browser meminta
3. Arahkan tangan ke kamera
4. Buat gestur isyarat — hasil tampil otomatis di panel kanan

---

## 🎯 Fitur yang Didukung

| Kategori      | Contoh                                           |
|---------------|--------------------------------------------------|
| Huruf         | A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z |
| Angka         | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10               |
| Kata          | teman-teman, bisa, belajar, sedikit, bahasa isyarat |

---

## 🔧 Konfigurasi

### Ganti URL Backend
Jika Flask berjalan di port berbeda, edit di `static/js/script.js`:
```javascript
const BACKEND_URL = 'http://localhost:5000';  // Ganti di sini
```

### Ubah Kecepatan Deteksi
Di `static/js/script.js`, ubah nilai (dalam milidetik):
```javascript
const CAPTURE_INTERVAL_MS = 300;  // 300ms = ~3 fps
```
- Lebih kecil = lebih cepat (tapi lebih berat)
- Lebih besar = lebih lambat (tapi lebih ringan)

---

## ❗ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| "Model tidak ditemukan" | Pastikan `bisindo_model.pkl` ada satu level di atas folder `bisindo_web/` |
| "Server tidak terhubung" | Pastikan `python app.py` sudah dijalankan |
| "Akses kamera ditolak" | Klik ikon kunci/kamera di address bar browser dan izinkan |
| "Tangan tidak terdeteksi" | Perbaiki pencahayaan dan jauhkan tangan dari latar sibuk |
| Prediksi tidak akurat | Pastikan model di-train dengan data yang cukup |

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask + Flask-CORS
- **Computer Vision**: OpenCV + MediaPipe Hands
- **Machine Learning**: Scikit-learn (model dari `bisindo_model.pkl`)
- **Komunikasi**: REST API + Fetch API + Base64 Image Transfer
