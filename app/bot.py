import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from transcribe import transcribe_short_audio, transcribe_long_audio
from audio_handler import download_audio, convert_audio_to_wav, get_audio_duration
from report_handler import save_report, extract_study_and_report
import operator_handler  # Asegúrate de importar operator_handler

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    from_number = request.form.get('From')
    msg = request.form.get('Body').strip().lower()
    num_media = int(request.form.get('NumMedia', 0))
    logging.debug(f"Mensaje recibido: {msg}")
    logging.debug(f"Número de archivos multimedia: {num_media}")
    logging.debug(f"Mensaje recibido de: {from_number}")

    response_message = ""

    if operator_handler.current_operator_id is None:
        if msg == "hola":
            response_message = "Hola, bienvenido. Por favor, proporciona tu ID de operador para iniciar sesión."
        else:
            success, message = operator_handler.login_operator(msg)
            response_message = message
    else:
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
                        duration = get_audio_duration(wav_path)
                        if duration is None:
                            response_message = "No se pudo obtener la duración del archivo de audio."
                        else:
                            if operator_handler.awaiting_audio:
                                response_message = operator_handler.save_audio(wav_path)
                                operator_handler.awaiting_audio = False
                            else:
                                response_message = "Por favor, selecciona una opción primero:\n1. Enviar un audio\n2. Eliminar el último audio"
        else:
            response_message = operator_handler.handle_operator_choice(msg)

    resp = MessagingResponse()
    resp.message(response_message)
    return str(resp)

def start_bot():
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    start_bot()
