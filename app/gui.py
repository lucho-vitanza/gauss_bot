import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os
import mimetypes
from transcribe import transcribe_short_audio
from audio_handler import convert_audio_to_wav, get_audio_duration
from report_handler import save_report, extract_study_and_report
from audios_gcs import transcribe_with_gcs  # Importar la función para transcripción con GCS

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

def start_gui():
    def open_file():
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                logging.info(f"Archivo seleccionado: {file_path}")
                content_type = mimetypes.guess_type(file_path)[0]
                if content_type is None:
                    messagebox.showerror("Error", "No se puede determinar el tipo de archivo.")
                    return

                wav_path = convert_audio_to_wav(file_path, content_type)
                if not wav_path:
                    messagebox.showerror("Error", "Error al convertir el archivo a WAV.")
                    return
                
                duration = get_audio_duration(wav_path)
                if duration is None:
                    messagebox.showerror("Error", "No se pudo obtener la duración del archivo de audio.")
                    return
                
                if duration <= 60:
                    transcript = transcribe_short_audio(wav_path)
                else:
                    transcript = transcribe_with_gcs(wav_path)  # Usar GCS para transcripción de audios largos
                
                if wav_path != file_path:
                    os.remove(wav_path)
                
                logging.debug(f"Transcripción: {transcript}")
                study_number, report_text = extract_study_and_report(transcript)
                save_path = save_report(study_number, report_text, "reports/")
                messagebox.showinfo("Guardado", f"Informe guardado en {save_path}")
        except Exception as e:
            logging.error("Error al abrir el archivo:", exc_info=True)
            messagebox.showerror("Error", f"Error al transcribir el audio: {e}")

    root = tk.Tk()
    root.title("Transcriptor Médico")
    root.geometry("500x300")
    
    open_button = tk.Button(root, text="Abrir Audio", command=open_file)
    open_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    logging.info("Iniciando GUI...")
    start_gui()
    logging.info("GUI finalizada.")
