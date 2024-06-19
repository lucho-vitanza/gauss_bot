import os
import logging
from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech
from audio_handler import convert_audio_to_wav, get_audio_duration

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

def upload_to_gcs(file_path, bucket_name, blob_name):
    """Sube un archivo a Google Cloud Storage."""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Subir archivo
        blob.upload_from_filename(file_path)

        logging.info(f"Archivo {file_path} subido exitosamente a {blob_name} en {bucket_name}.")
        return True
    except Exception as e:
        logging.error(f"Error al subir archivo a Google Cloud Storage: {e}")
        return False

def transcribe_with_gcs(file_path):
    """Sube el archivo a GCS y lo transcribe usando la API de Google Speech-to-Text."""
    try:
        bucket_name = os.getenv('GCS_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("El nombre del bucket de GCS no está configurado en las variables de entorno.")
        
        blob_name = os.path.basename(file_path)

        # Subir el archivo a GCS
        if not upload_to_gcs(file_path, bucket_name, blob_name):
            return None

        # Construir URI de GCS
        gcs_uri = f"gs://{bucket_name}/{blob_name}"
        
        # Configurar cliente de Speech-to-Text
        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="es-ES",
            enable_automatic_punctuation=True
        )

        # Realizar la transcripción
        operation = client.long_running_recognize(config=config, audio=audio)
        logging.info("Esperando a que la operación termine...")
        response = operation.result(timeout=600)

        # Procesar y devolver la transcripción
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "

        logging.info(f"Transcripción completada: {transcript}")
        return transcript.strip()
    except Exception as e:
        logging.error(f"Error en la transcripción con GCS: {e}")
        return None
