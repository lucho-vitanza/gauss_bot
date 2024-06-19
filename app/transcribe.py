from google.cloud import speech_v1p1beta1 as speech
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

def transcribe_short_audio(file_path):
    logging.info(f"Iniciando transcripción para el archivo corto: {file_path}")
    
    client = speech.SpeechClient()
    
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
    
    logging.debug(f"Tamaño del archivo de audio leído: {len(content)} bytes")
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='es-ES'
    )

    response = client.recognize(config=config, audio=audio)
    
    logging.debug(f"Respuesta recibida de Google Cloud Speech-to-Text: {response}")
    
    if response.results:
        transcript = '\n'.join([result.alternatives[0].transcript for result in response.results])
        logging.info(f"Transcripción obtenida: {transcript}")

        line_count = len(response.results)
        logging.info(f"Cantidad de líneas en la transcripción: {line_count}")

        return transcript
    else:
        logging.warning("La transcripción está vacía.")
        return ""

def transcribe_long_audio(file_path):
    logging.info(f"Iniciando transcripción para el archivo largo: {file_path}")
    
    client = speech.SpeechClient()
    
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
    
    logging.debug(f"Tamaño del archivo de audio leído: {len(content)} bytes")
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='es-ES',
        enable_automatic_punctuation=True  # Opcional: habilita puntuación automática
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    logging.info("Esperando a que la operación de reconocimiento a largo plazo se complete...")
    response = operation.result(timeout=600)  # Timeout ajustable según sea necesario
    
    logging.debug(f"Respuesta recibida de Google Cloud Speech-to-Text: {response}")
    
    if response.results:
        transcript = '\n'.join([result.alternatives[0].transcript for result in response.results])
        logging.info(f"Transcripción obtenida: {transcript}")

        line_count = len(response.results)
        logging.info(f"Cantidad de líneas en la transcripción: {line_count}")

        return transcript
    else:
        logging.warning("La transcripción está vacía.")
        return ""
