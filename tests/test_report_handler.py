import sys
import os

# Agregar el directorio 'app' al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Ahora podemos importar las funciones desde report_handler.py
from report_handler import extract_study_and_report, save_report

import logging

# Configurar el logger
logging.basicConfig(level=logging.DEBUG)

# Transcripción de prueba
transcript = """
numero estudio: 00324325435
La paciente tiene 92mm de diametro en su arteria principal. No se observan anomalías significativas.
"""

# Llamar a la función extract_study_and_report
study_number, report_text = extract_study_and_report(transcript)

# Imprimir los resultados
print("Número de Estudio:", study_number)
print("Texto del Informe:", report_text)

# Guardar el informe (opcional)
directory = "./reports"
file_path = save_report(study_number, report_text, directory)
print(f"Informe guardado en: {file_path}")

