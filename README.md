# 🎙️ Auto-Notulen Rapat AI (Whisper + Gemini)

Aplikasi web cerdas berbasis AI yang menggabungkan kemampuan pemrosesan suara (Audio Processing) dan pemrosesan teks (NLP) untuk mengotomatiskan pembuatan notulen rapat. 

Sistem ini akan mentranskripsikan rekaman audio rapat menjadi teks secara lokal menggunakan **OpenAI Whisper**, kemudian merangkum poin-poin utama dan mengekstrak *Action Items* menggunakan **Google Gemini API**.

## 🚀 Fitur Utama

**Transkripsi Luring (Offline-Ready):** Menggunakan model `Whisper (Base)` yang berjalan di perangkat Anda sendiri untuk privasi data suara yang terjamin.
**Ringkasan Cerdas:** Ditenagai oleh `Gemini 1.5 Flash` untuk merangkum hasil transkripsi menjadi Ringkasan Eksekutif.
**Ekstraksi Action Item:** Otomatis mendeteksi dan mendaftar tugas-tugas yang didelegasikan selama rapat berlangsung beserta penanggung jawabnya.
**Antarmuka Pengguna Intuitif:** Dibangun menggunakan `Gradio` untuk kemudahan unggah file audio dan pembacaan hasil.
**Deployment Instan:** Dilengkapi dengan *Omega-Code Deployment Script* (`build.js`) berbasis Node.js untuk instalasi satu klik.

## 🛠️ Tech Stack

**Core Logic:** Python 3
**Deployment Builder:** Node.js
**Audio Processing:** [OpenAI Whisper](https://github.com/openai/whisper)
**LLM Engine:** [Google Generative AI (Gemini)](https://ai.google.dev/)
**Frontend UI:** [Gradio](https://www.gradio.app/)

## 📋 Prasyarat Sistem

Sebelum menginstal dan menjalankan aplikasi, pastikan sistem Anda sudah terinstal:
1.  **Python 3.8+** (Direkomendasikan Python 3.11 atau lebih baru). Pastikan Python sudah ditambahkan ke dalam `PATH` OS Anda.
2.  **FFmpeg** (Wajib untuk pemrosesan file audio di Windows/Linux).
    * *Pengguna Windows:* Unduh FFmpeg, ekstrak, dan tambahkan path folder `bin` ke dalam Environment Variables OS Anda.

## ⚙️ Instalasi & Konfigurasi

## 1. Kloning repositori ini:
git clone [https://github.com/albetpf/auto-notulen-ai.git](https://github.com/albetpf/SISTEM-AUTO-NOTULEN-RAPAT-MENGGUNAKAN-WHISPER-GEMINI.git)
cd SISTEM-AUTO-NOTULEN-RAPAT-MENGGUNAKAN-WHISPER-GEMINI

## 2. Instal dependensi:
python -m pip install -r requirements.txt

## 3. Buka file app.py menggunakan teks editor Anda dan masukkan API Key Gemini Anda pada baris ini:
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "API_KEY_GEMINI")

## 🖥️ Cara Penggunaan
Buka terminal di folder proyek dan jalankan:
python app.py
Tunggu hingga terminal memunculkan alamat server lokal (biasanya http://127.0.0.1:7860).
Buka alamat tersebut di web browser Anda.
Unggah file audio (berformat MP3, WAV, atau M4A) ke dalam kolom yang disediakan.
Klik tombol "🚀 Proses Notulen".
Model AI akan memproses data Anda. Hasil Transkripsi Mentah, Ringkasan, dan Action Items akan muncul di panel sebelah kanan dan siap untuk disalin.

## ⚠️ Catatan Penting
Kecepatan Pemrosesan: Kecepatan transkripsi sangat bergantung pada spesifikasi CPU/GPU komputer Anda. Model Whisper base digunakan untuk keseimbangan antara kecepatan dan performa pada komputer standar.

Kualitas Audio: Pastikan rekaman audio cukup jernih tanpa terlalu banyak gangguan (noise) latar belakang agar transkripsi Whisper lebih akurat dan ringkasan Gemini lebih relevan.

## 📄 Lisensi
MIT License - Silakan gunakan, modifikasi, dan distribusikan proyek ini secara bebas untuk kebutuhan personal maupun komersial.
   
