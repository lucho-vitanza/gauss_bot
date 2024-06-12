import subprocess
from dotenv import load_dotenv

def main():
    load_dotenv()  # Cargar variables de entorno desde el archivo .env

    # Ejecutar GUI en un nuevo proceso
    gui_process = subprocess.Popen(['gnome-terminal', '--', 'bash','-c' , 'python3 ./gui.py; exec bash'])
    
    # Ejecutar servidor Flask en un nuevo proceso
    flask_process = subprocess.Popen(['gnome-terminal', '--','bash','-c','python3 ./bot.py; exec bash'])

    # Esperar a que los procesos terminen (opcional)
    gui_process.wait()
    flask_process.wait()

if __name__ == "__main__":
    main()
