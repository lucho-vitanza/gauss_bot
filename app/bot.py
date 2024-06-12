import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from transcribe import transcribe_audio
from audio_handler import download_audio, convert_audio_to_wav
from report_handler import save_report, extract_study_and_report

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body')
    num_media = int(request.form.get('NumMedia', 0))
    logging.debug(f"Mensaje recibido: {msg}")
    logging.debug(f"Número de archivos multimedia: {num_media}")

    if num_media > 0:
        media_url = request.form.get('MediaUrl0')
        logging.debug(f"Media URL: {media_url}")

        if media_url:
            audio_path, media_content_type = download_audio(media_url)
            logging.debug(f"Audio descargado en: {audio_path}")

            if not audio_path:
                response_message = "Error al descargar el archivo de audio."
            else:
                wav_path = convert_audio_to_wav(audio_path, media_content_type)
                if not wav_path:
                    response_message = "Error al convertir el archivo de audio."
                else:
                    transcript = transcribe_audio(wav_path)
                    logging.debug(f"Transcripción: {transcript}")

                    study_number, report_text = extract_study_and_report(transcript)
                    save_path = save_report(study_number, report_text, "reports/")
                    response_message = f"Informe guardado en {save_path}"
        else:
            response_message = "No se pudo obtener la URL del archivo multimedia."
    else:
        response_message = "Por favor envíe un audio."

    resp = MessagingResponse()
    resp.message(response_message)
    return str(resp)

def start_bot():
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    start_bot()
