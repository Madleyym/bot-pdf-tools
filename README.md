# Bot Penerjemah PDF

Bot penerjemah PDF otomatis dari bahasa Inggris ke bahasa Indonesia menggunakan Google Translate API.

## Cara Cepat Mulai (Quick Start)

1. **Download dan Ekstrak**
   ```bash
   git clone https://github.com/Madleyym/bot-pdf-tools.git
   cd bot-pdf-tools
   ```

2. **Install Python** (jika belum)
   - Download Python 3.x dari [python.org](https://www.python.org/downloads/)
   - Pastikan centang "Add Python to PATH" saat instalasi

3. **Install Dependencies**
   ```bash
   pip install PyPDF2 deep-translator fpdf
   ```

4. **Siapkan File**
   - Buat folder `PDF` jika belum ada
   - Copykan file PDF berbahasa Inggris ke folder `PDF`

5. **Jalankan Bot**
   ```bash
   python bot.py
   ```

## Panduan Lengkap

### Persiapan Awal

1. **Install Git** (jika belum)
   - Download dari [git-scm.com](https://git-scm.com/downloads)
   - Install dengan pengaturan default

2. **Clone Repository**
   ```bash
   git clone https://github.com/Madleyym/bot-pdf-tools.git
   ```

3. **Buka Terminal/Command Prompt**
   - Windows: `Win + R`, ketik `cmd`, Enter
   - Mac: Buka Terminal
   - Linux: Ctrl + Alt + T

4. **Masuk ke Direktori**
   ```bash
   cd path/to/bot-pdf-tools
   ```

### Install Dependencies

1. **Periksa Python**
   ```bash
   python --version
   ```
   Harus menampilkan Python 3.x

2. **Periksa pip**
   ```bash
   pip --version
   ```

3. **Install Package yang Diperlukan**
   ```bash
   pip install PyPDF2 deep-translator fpdf
   ```

### Menyiapkan File

1. **Struktur Folder**
   ```
   bot-pdf-tools/
   │
   ├── PDF/                    # Folder untuk file input
   ├── partial_translations/   # Akan dibuat otomatis
   └── bot.py
   ```

2. **Format File yang Didukung**
   - File PDF dengan teks yang bisa dicopy
   - Ukuran file: tidak ada batasan khusus
   - Bahasa: Inggris (sumber)

### Menjalankan Bot

1. **Mode Dasar**
   ```bash
   python bot.py
   ```

2. **Memantau Progress**
   - Progress ditampilkan per halaman
   - Persentase penyelesaian
   - Statistik sukses/gagal

3. **Menghentikan Proses**
   - Tekan `Ctrl + C` untuk pause
   - Progress tersimpan otomatis

4. **Melanjutkan Proses**
   - Jalankan ulang bot
   - Akan melanjutkan dari halaman terakhir

### Troubleshooting

1. **Error "ModuleNotFoundError"**
   ```bash
   pip install --upgrade PyPDF2 deep-translator fpdf
   ```

2. **Error Permission**
   - Jalankan terminal sebagai Administrator (Windows)
   - Gunakan `sudo` (Linux/Mac)

3. **File Tidak Terbaca**
   - Pastikan file PDF bisa dicopy textnya
   - Coba scan ulang jika dari hasil scan

4. **Koneksi Internet**
   - Cek koneksi internet
   - Gunakan koneksi stabil

### Tips Penggunaan

1. **Optimasi Kinerja**
   - Proses satu file besar sekaligus
   - Biarkan bot berjalan hingga selesai
   - Gunakan koneksi internet stabil

2. **Mengecek Hasil**
   - Cek folder `partial_translations` untuk hasil per halaman
   - File final ada di folder utama dengan prefix "translated_"

3. **Backup Progress**
   - File progress tersimpan dalam format JSON
   - Bisa dicopy untuk backup

## Informasi Teknis

- **Author**: Madleyym
- **Version**: 1.0.0
- **Created**: 2025-02-27
- **Python Version**: 3.x
- **Dependencies**: PyPDF2, deep-translator, fpdf

## Support

Jika mengalami masalah:
1. Buka issue di GitHub
2. Jelaskan error yang muncul
3. Lampirkan log error jika ada
4. Sebutkan versi Python dan OS yang digunakan

## Update Log

- **2025-02-27**: Initial release
- Penambahan fitur progress tracking
- Penambahan penyimpanan parsial
- Peningkatan stabilitas

## Lisensi

MIT License - Lihat file LICENSE untuk detail lengkap.