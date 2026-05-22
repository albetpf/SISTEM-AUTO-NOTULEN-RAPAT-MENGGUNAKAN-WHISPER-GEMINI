import gradio as gr
import whisper
import os
import warnings
# Menggunakan SDK Google terbaru
from google import genai

# Mengabaikan warning fp16 pada CPU
warnings.filterwarnings("ignore")

# Konfigurasi API Gemini (SDK Baru)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "API_KEY_GEMINI")
client = genai.Client(api_key=GEMINI_API_KEY)

# --- WADAH KOSONG UNTUK LAZY LOADING WHISPER ---
whisper_model = None
# -----------------------------------------------

def process_audio(audio_filepath):
    global whisper_model # Memanggil wadah global

    if audio_filepath is None:
        return "Gagal: Tidak ada file audio yang diunggah.", "Gagal: Tidak ada ringkasan.", None

    try:
        # --- TEKNIK LAZY LOADING ---
        # AI hanya dimuat SAAT tombol diklik pertama kali, membuat Hot Reloading kilat!
        if whisper_model is None:
            print("[System] Memuat model AI Whisper (Small) ke memori utama untuk pertama kalinya...")
            whisper_model = whisper.load_model("small")
        # ---------------------------

        # Tahap 1: Transkripsi Audio dengan Whisper
        print("[System] Memulai proses transkripsi, mohon tunggu...")
        prompt_bocoran = "Tes 1 2. Ini adalah rekaman percakapan pengujian notulen rapat menggunakan AI, Whisper, dan Gemini."
        
        result = whisper_model.transcribe(
            audio_filepath, 
            language="id", 
            condition_on_previous_text=False,
            initial_prompt=prompt_bocoran,
            no_speech_threshold=0.6
        )
        transcript = result["text"]
        
        # Proteksi halusinasi audio kosong/noise
        if not transcript.strip() or len(transcript.strip()) < 15:
            return "Audio terlalu hening atau tidak terdeteksi suara percakapan yang jelas (Noise/Silence).", "Transkripsi gagal, tidak ada data untuk dirangkum.", None

        # Tahap 2: Meringkas dengan Gemini API (Menggunakan format GenAI terbaru)
        print("[System] Menghubungkan ke Gemini API (SDK Baru)...")
        
        prompt = f"""
        Anda adalah asisten notulis rapat yang profesional. 
        Berikut adalah transkripsi mentah dari sebuah rapat/wawancara. 
        
        PERINGATAN PENTING: Jika teks di bawah ini terlihat seperti karakter acak, bahasa asing yang tidak masuk akal, atau hasil halusinasi mesin yang ngawur, JANGAN mencoba memaksa untuk merangkumnya. Cukup balas dengan pesan: "Transkripsi gagal: Audio tidak mengandung percakapan yang dapat dikenali mesin."

        Jika teksnya masuk akal dan berbahasa manusia yang wajar, tolong buatkan:
        1. Ringkasan Eksekutif (Poin-poin utama yang dibahas).
        2. Action Items (Daftar tugas yang harus dilakukan selanjutnya dan oleh siapa).

        Transkripsi Rapat:
        {transcript}
        """
        
        try:
            # Menggunakan model gemini-2.5-flash (versi teringan dan tercerdas saat ini)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            summary = response.text
        except Exception as e:
            summary = f"[ERROR API] Gagal merangkum teks. Detail error: {str(e)}"
            
        print("[System] Menyimpan hasil ke file...")
        output_filename = "Hasil_Notulen.txt"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("=== RINGKASAN & ACTION ITEMS ===\n")
            f.write(summary + "\n\n")
            f.write("=== TRANSKRIPSI MENTAH ===\n")
            f.write(transcript)
            
        print("[System] Pemrosesan selesai!")
        return transcript, summary, output_filename

    except Exception as e:
        return f"[ERROR SISTEM] Terjadi kesalahan saat memproses audio: {str(e)}", "Proses dibatalkan karena error.", None


# Script Anti-Refresh
js_peringatan_refresh = """
function() {
    window.addEventListener('beforeunload', function (e) {
        e.preventDefault();
        e.returnValue = '';
    });
}
"""

with gr.Blocks(title="Omega Notulen AI", theme=gr.themes.Soft(), js=js_peringatan_refresh) as demo:
    gr.Markdown("# 🎙️ Sistem Auto-Notulen Rapat (Whisper + Gemini)")
    gr.Markdown("Unggah rekaman audio rapat Anda. Sistem akan mengetik ulang semua percakapan secara otomatis, menyusun poin penting, dan membuat file unduhan.")
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(type="filepath", label="Unggah Berkas Audio (MP3, WAV, M4A)")
            process_btn = gr.Button("🚀 Proses Notulen", variant="primary")
            gr.Markdown("**Catatan:** *Pastikan Anda sudah mengganti GEMINI_API_KEY di dalam script app.py.*")
        
        with gr.Column(scale=2):
            with gr.Accordion("Hasil Transkripsi Mentah", open=False):
                transcript_output = gr.Textbox(label="Teks Penuh Rapat", lines=8)
            summary_output = gr.Textbox(label="Ringkasan & Action Items", lines=15)
            file_output = gr.File(label="📥 Download Hasil Notulen (.txt)")
            
    process_btn.click(
        fn=process_audio, 
        inputs=audio_input, 
        outputs=[transcript_output, summary_output, file_output]
    )

if __name__ == "__main__":
    print("[Server] Menjalankan Web UI... (Cek alamat URL di terminal)")
    demo.queue().launch(server_name="127.0.0.1", inbrowser=True)
