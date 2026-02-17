# Tucil1_13524107 - Queens LinkedIn Solver

**Penyelesai Puzzle Queens LinkedIn dengan Algoritma Brute Force & Backtracking**

Program ini adalah aplikasi GUI berbasis Python untuk menyelesaikan permainan puzzle "Queens" (seperti yang ada di LinkedIn Games). Program ini dapat mencari solusi penempatan Queen yang valid pada papan N×N dengan constraint warna wilayah (region), baris/kolom unik, dan aturan "tidak boleh bersentuhan" (termasuk diagonal 1 langkah).

## 📋 Deskripsi Masalah

Diberikan papan berukuran N×N yang terbagi menjadi N wilayah warna berbeda. Tujuan permainan adalah menempatkan **satu Queen di setiap baris, setiap kolom, dan setiap wilayah warna**, dengan syarat tambahan:
- Tidak ada dua Queen yang saling bersentuhan (termasuk secara diagonal).

## 🚀 Fitur Utama

- **GUI Interaktif**: Tampilan visual papan permainan.
- **Dua Algoritma**:
  - **Brute Force**: Mencoba semua kemungkinan penempatan secara exhaustive.
  - **Optimized (Backtracking)**: Penyelesaian lebih cepat dengan pemangkasan (pruning) cabang yang tidak valid.
- **Input Fleksibel**:
  - **Load .txt**: Membaca konfigurasi papan dari file teks.
  - **Load Image**: Membaca konfigurasi papan langsung dari **Screenshot** permainan (Support deteksi grid otomatis!).
- **Visualisasi**: Animasi langkah penyelesaian (bisa diatur kecepatannya).
- **Export Hasil**: Simpan solusi ke file `.txt` atau gambar `.png`.

## 🛠️ Requirements

Program ini berjalan di **Python 3.x**.
Library tambahan yang diperlukan:
- `Pillow` (untuk pemrosesan gambar)
- `tkinter` (biasanya sudah termasuk dalam instalasi Python standar)

## 📦 Instalasi

1. **Clone repository ini**:
   ```bash
   git clone https://github.com/ravasrgh/Tucil1_13524107.git
   cd Tucil1_13524107
   ```

2. **Install dependencies**:
   ```bash
   pip install pillow
   ```
   *(Jika menggunakan macOS dan mengalami error Tkinter, pastikan menginstall python-tk: `brew install python-tk`)*

## ▶️ Cara Menjalankan

Jalankan file utama program (`tucil1.py`) melalui terminal:

```bash
python src/tucil1.py
```
*(atau `python3 src/tucil1.py` tergantung konfigurasi sistem Anda)*

## 🎮 Cara Menggunakan

1. **Buka Program**: Jalankan perintah di atas.
2. **Load Papan**:
   - Klik **📂 Load .txt** untuk membuka file konfigurasi teks.
   - Klik **🖼 Load Image** untuk membuka screenshot puzzle (pastikan gambar grid terlihat jelas).
3. **Pilih Algoritma**:
   - Pilih radio button **Brute Force** atau **Optimized**.
4. **Atur Kecepatan (Opsional)**:
   - Geser slider untuk mempercepat atau memperlambat visualisasi pencarian solusi.
5. **Mulai Penyelesaian**:
   - Klik tombol **▶ Solve**.
   - Tombol **⏹ Stop** bisa digunakan untuk menghentikan proses di tengah jalan.
6. **Simpan Solusi**:
   - Setelah solusi ditemukan, klik **💾 Save** untuk menyimpan hasil sebagai file teks atau gambar.

## 📄 Format Input File (.txt)

File input harus berupa grid karakter N×N, di mana setiap karakter merepresentasikan warna wilayah (region) sel tersebut.

Contoh `input.txt` (4x4):
```text
AAAA
BBBB
CCCC
DDDD
```

## 👤 Author

**Rava Khoman Tuah Saragih**
**NIM: 13524107**
Program Studi Teknik Informatika
Institut Teknologi Bandung
