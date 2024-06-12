import os
import logging
import re

def extract_study_and_report(transcript):
    logging.debug(f"TRANSCRIPCION AL INICIO DE LA FUNCION: {transcript}")
    lines = transcript.split("\n")
    study_number = lines[0].strip() if lines else "no_identificado"
    report_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else transcript.strip()
    logging.debug(f"report text: {report_text}")
    return study_number, report_text



def save_report(study_number, report_text, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Limpiar y limitar el número del estudio para el nombre del archivo
    study_number = re.sub(r'[^A-Za-z0-9]+', '_', study_number[:10])  # Reemplazar caracteres especiales con '_'
    file_path = os.path.join(directory, f"{study_number}.txt")
    
    try:
        with open(file_path, "w") as file:
            file.write(report_text)
        logging.info(f"Informe guardado en: {file_path}")
    except Exception as e:
        logging.error(f"Error al guardar el informe: {e}", exc_info=True)
    
    return file_path
