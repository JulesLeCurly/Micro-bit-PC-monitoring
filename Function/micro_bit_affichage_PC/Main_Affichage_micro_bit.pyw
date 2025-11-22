import serial
import serial.tools.list_ports
import time
import threading
import pystray
from pystray import MenuItem, Menu
from PIL import Image
import mmap
import json
import os


UPDATE_INTERVAL = 0.25

# Port série du micro:bit (remplacez par votre port)
microbit_port = 'COM3'  # Windows : COMx ; macOS/Linux : /dev/ttyACMx
baud_rate = 115200  # Doit correspondre au paramètre côté micro:bit

# Utiliser un chemin valide pour Windows
SHARED_FILE = os.path.join(os.getenv("TEMP", "C:\\temp"), "metrics_shared")

# Créer le dossier s'il n'existe pas
os.makedirs(os.path.dirname(SHARED_FILE), exist_ok=True)

MMAP_SIZE = 4096  # Taille identique à celle définie dans le producteur

# Envoyer des données au micro:bit
running = True
print("running")

serial.Serial(microbit_port, baud_rate, timeout=1)

def call_API():
    with open(SHARED_FILE, "r+b") as f:
        mem = mmap.mmap(f.fileno(), MMAP_SIZE)

        while True:
            mem.seek(0)
            status = mem.read(1)  # Lire le marqueur
            if status == b'\x02':  # 2 = données prêtes
                raw_data = mem.read(MMAP_SIZE - 1).rstrip(b'\x00')
                mem.close()
                try:
                    metrics = json.loads(raw_data.decode('utf-8'))
                    return metrics
                except json.JSONDecodeError:
                    print("Erreur : Données corrompues ou incomplètes.")
            else:
                # Données en cours d'écriture, attente...
                time.sleep(0.05)

def wait_for_start():
    try:
        serial.Serial(microbit_port, baud_rate, timeout=1)
        collect_data()
    except serial.serialutil.SerialException:
        time.sleep(1)
        if running:
            wait_for_start()

def disconnected():
    icon.icon = Image.open("color/red.jpg")
    time.sleep(2) # Wait if the probleme can be fixed itself
    wait_for_start()

def collect_data():
    time.sleep(0.2)
    try:
        with serial.Serial(microbit_port, baud_rate, timeout=1) as ser:
            icon.icon = Image.open("color/green.jpg")
            while running:
                metrics = call_API()
                cpu_prc = metrics["cpu_usage"]
                mem_prc = metrics["memory"]["percent"]
                gpu_prc = metrics["gpu"]["usage"]

                message = f"{cpu_prc}:{mem_prc}:{gpu_prc}"

                ser.write(message.encode("utf-8"))  # Envoi au micro:bit
                time.sleep(UPDATE_INTERVAL)  # Pause d'1 seconde

    except:
        disconnected()

def quit_action(icon, item):
    global running
    running = False
    icon.stop()

def create_menu(): 
    menu = Menu(
        MenuItem("Quitter", quit_action)
    )
    return menu

icon = pystray.Icon("system_monitor", Image.open("color/red.jpg"), "CPU/GPU/MEM Live ;)", create_menu())

data_thread = threading.Thread(target=wait_for_start, daemon=True)
data_thread.start()

icon.run()