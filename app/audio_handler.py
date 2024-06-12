import os
import requests
import mimetypes
import subprocess
import logging

def download_audio(url):
    response = requests.get(url, auth=(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN')))
    if response.status_code == 200 and response.headers['Content-Type'].startswith('audio/'):
        audio_content = response.content
        content_type = response.headers['Content-Type']
        extension = mimetypes.guess_extension(content_type)
        file_path = f"temp_audio{extension}"
        with open(file_path, 'wb') as file:
            file.write(audio_content)
        logging.debug(f"Archivo de audio guardado en: {file_path} con tamaño: {len(audio_content)} bytes")
        return file_path, content_type
    else:
        logging.error("El contenido descargado no coincide con el tipo de contenido esperado.")
        return None, None

def convert_audio_to_wav(input_file_path, content_type, output_dir="temp_audio"):
    if content_type == 'audio/wav':
        return input_file_path
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    wav_file_path = os.path.join(output_dir, f"{base_name}.wav")
    command = ['ffmpeg', '-i', input_file_path, '-c:a', 'pcm_s16le', '-ar', '16000', wav_file_path]
    
    try:
        subprocess.run(command, check=True)
        logging.debug(f"Archivo convertido a WAV: {wav_file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al convertir el archivo a WAV: {e}")
        return None
    
    return wav_file_path
