# Bot Penerjemah PDF

Sebuah alat berbasis Python yang secara otomatis menerjemahkan dokumen PDF dari bahasa Inggris ke bahasa Indonesia menggunakan Google Translate API.

## Fitur

- 🔄 Penerjemahan dari bahasa Inggris ke Indonesia
- 📚 Pemrosesan batch untuk banyak file PDF
- 📁 Output yang terorganisir dengan prefix "translated_"
- 📊 Pelacakan progres selama penerjemahan
- ⚡ Pemrosesan cepat
- 🛠️ Penanganan kesalahan yang kuat

## Prasyarat

Sebelum menjalankan alat ini, pastikan Anda memiliki:
- Python 3.x terinstal
- Koneksi internet (diperlukan untuk penerjemahan)

## Instalasi

1. Clone repositori ini:
```bash
git clone https://github.com/Madleyym/bot-pdf-tools.git
cd bot-pdf-tools
```

2. Instal dependensi yang diperlukan:
```bash
pip install PyPDF2 deep-translator fpdf
```

## Struktur Direktori

```
bot-pdf-tools/
│
├── PDF/                    # Letakkan file PDF berbahasa Inggris di sini
├── bot.py                 # Skrip utama
└── README.md              # File ini
```

## Cara Penggunaan

1. Letakkan file PDF berbahasa Inggris Anda di folder `PDF`.

2. Jalankan skrip:
```bash
python bot.py
```

3. Skrip akan:
   - Memproses semua file PDF berbahasa Inggris di folder PDF
   - Menerjemahkan kontennya ke bahasa Indonesia
   - Membuat versi terjemahan dengan prefix "translated_"
   - Menampilkan progres untuk setiap file dan halaman
   - Menampilkan ringkasan hasil penerjemahan yang sukses dan gagal

## Konfigurasi

Skrip ini dikonfigurasi untuk:
- Membaca PDF berbahasa Inggris dari: `Folder: PDF`
- Menerjemahkan dari bahasa Inggris ke bahasa Indonesia
- Menyimpan file terjemahan di folder yang sama dengan prefix "translated_"

## Penanganan Kesalahan

Skrip ini mencakup penanganan kesalahan yang komprehensif untuk:
- File atau folder PDF yang hilang
- Kesalahan dalam penerjemahan
- Masalah akses file
- Kesalahan saat membaca/menulis PDF

## Contoh Output

File input: `chapter1.pdf` (Bahasa Inggris)
File output: `translated_chapter1.pdf` (Bahasa Indonesia)

## Kontribusi

Silakan:
- Laporkan masalah
- Kirimkan pull request
- Berikan saran perbaikan
- Bagikan umpan balik Anda

## Penulis

- **Mad-jr**

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail lebih lanjut.

## Penghargaan

- PyPDF2 untuk pemrosesan PDF
- deep-translator untuk layanan penerjemahan
- FPDF untuk pembuatan PDF

## Catatan Penting

1. Alat ini khusus dirancang untuk penerjemahan dari bahasa Inggris ke bahasa Indonesia
2. Pastikan file PDF Anda berisi teks bahasa Inggris yang dapat dibaca
3. Kualitas terjemahan tergantung pada akurasi Google Translate
4. File PDF berukuran besar mungkin membutuhkan waktu lebih lama untuk diproses