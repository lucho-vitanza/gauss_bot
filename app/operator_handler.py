import os
import logging
import time

# Simulación de base de datos de operadores
OPERATORS_DB = {
    "12345": "Operador 1",
    "67890": "Operador 2"
}

# Variables para el manejo del estado del operador
current_operator_id = None
awaiting_audio = False
delete_last_audio = False
last_audio_path = None

def login_operator(operator_id):
    global current_operator_id
    if operator_id in OPERATORS_DB:
        current_operator_id = operator_id
        logging.info(f"Operador {OPERATORS_DB[operator_id]} ha iniciado sesión.")
        return True, f"Bienvenido {OPERATORS_DB[operator_id]}. ¿Qué deseas hacer?\n1. Enviar un audio\n2. Eliminar el último audio"
    else:
        return False, "ID de operador no válido. Por favor, intenta nuevamente."

def handle_operator_choice(choice):
    global awaiting_audio, delete_last_audio
    if choice == "1":
        awaiting_audio = True
        return "Te escucho."
    elif choice == "2":
        delete_last_audio = True
        return "El último audio será eliminado."
    else:
        return "Opción no válida. Por favor, elige 1 o 2."

def save_audio(audio_path):
    global last_audio_path
    last_audio_path = audio_path
    # Aquí puedes añadir la lógica para almacenar el audio localmente
    time.sleep(5)  # Espera antes de enviar el audio para simular almacenamiento
    return "Audio recibido y almacenado."

def get_last_audio_path():
    return last_audio_path

def should_delete_last_audio():
    return delete_last_audio

def reset_delete_flag():
    global delete_last_audio
    delete_last_audio = False
