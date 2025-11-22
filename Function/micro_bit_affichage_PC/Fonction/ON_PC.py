import time
import mmap
import json
import os

UPDATE_INTERVAL = 0.25

# Utiliser un chemin valide pour Windows
SHARED_FILE = os.path.join(os.getenv("TEMP", "C:\\temp"), "metrics_shared")

# Créer le dossier s'il n'existe pas
os.makedirs(os.path.dirname(SHARED_FILE), exist_ok=True)

MMAP_SIZE = 4096  # Taille identique à celle définie dans le producteur

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


def main():
    metrics = call_API()
    cpu_prc = metrics["cpu_usage"]
    mem_prc = metrics["memory"]["percent"]
    gpu_prc = metrics["gpu"]["usage"]
    gpu_temp = metrics["gpu"]["temperature"]

    message = f"{cpu_prc}:{mem_prc}:{gpu_prc}:{gpu_temp}"
    return message.encode("utf-8")

