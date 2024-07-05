import os
import re
import logging
import Levenshtein

def extract_study_and_report(transcript):
    logging.debug(f"TRANSCRIPCION AL INICIO DE LA FUNCION: {transcript}")
    
    # Frases clave que buscamos encontrar
    # Para este caso, podrías tener una lista predefinida de patrones de estudio que suelen aparecer.
    frases_clave = ["numero de estudio: ", "número de estudio", "numero estudio","numer estudi","numero estudi"]
    
    # Inicializar valores predeterminados
    study_number = "no_identificado"
    report_text = transcript.strip()

    mejor_similitud = 0.0
    mejor_texto = None

    # Verificar si la transcripción contiene el número de estudio
    for frase in frases_clave:
        if frase in transcript:
            start_index = transcript.find(frase) + len(frase)
            end_index = start_index + 20  # Asumimos que el número de estudio tiene una longitud máxima de 20 caracteres
            posible_numero = transcript[start_index:end_index]
            posible_numero = re.findall(r'\d+', posible_numero)  # Extraer solo los dígitos
            if posible_numero:
                study_number = posible_numero[0]  # Tomamos el primer grupo de dígitos como el número de estudio
                break

    # Opción alternativa: utilizar Levenshtein ratio para encontrar similitudes
    #if mejor_similitud == 0.0:
    #    for index in range(len(transcript)):
    #        subcadena = transcript[index:index+20]  # Tomamos subcadenas de 20 caracteres
    #        for frase in frases_clave:
    #            similitud = Levenshtein.ratio(subcadena.lower(), frase.lower())
    #            if similitud > mejor_similitud:
    #                mejor_similitud = similitud
    #                mejor_texto = subcadena

        if mejor_texto:
            study_number = re.findall(r'\d+', study_number)
            study_number = study_number[0] if study_number else "no_identificado"

    lines = transcript.split("\n")
    report_text = "\n".join(lines).strip() if lines else transcript.strip()
    logging.debug(f"report text: {report_text}")
    logging.debug(f"numero de estudio: {study_number}")
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
