import os
import mmap
import json
import psutil
import pynvml
import time
import wmi
from threading import Event

# Définition des constantes
SHARED_FILE = os.path.join(os.getenv("TEMP", "C:\\temp"), "metrics_shared")
STOP_SIGNAL_FILE = os.path.join(os.getenv("TEMP", "C:\\temp"), "stop_signal")
MMAP_SIZE = 4096
UPDATE_INTERVAL = 0.25

os.makedirs(os.path.dirname(SHARED_FILE), exist_ok=True)

def init_nvml():
    """Initialisation de NVML avec gestion des erreurs."""
    try:
        pynvml.nvmlInit()
        return True
    except pynvml.NVMLError as e:
        print(f"Erreur NVML : {e}")
        return False

def get_gpu_metrics():
    """Récupère l'utilisation et la température du GPU si disponible."""
    if not gpu_available:
        return {"error": "GPU not available"}
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        return {"usage": util.gpu, "temperature": temp, "fan_speed": fan_speed}
    except pynvml.NVMLError as e:
        return {"error": str(e)}

def collect_and_write_metrics():
    """Collecte les métriques et les écrit dans la mémoire partagée."""
    with open(SHARED_FILE, "wb") as f:
        f.write(b'\x00' * MMAP_SIZE)
    
    with open(SHARED_FILE, "r+b") as f:
        mem = mmap.mmap(f.fileno(), MMAP_SIZE)
        while not should_stop.is_set():
            if os.path.exists(STOP_SIGNAL_FILE):
                print("Arrêt manuel détecté.")
                should_stop.set()
                break
            
            metrics = {
                "cpu_usage": psutil.cpu_percent(),
                "memory": {"percent": psutil.virtual_memory().percent},
                "gpu": get_gpu_metrics(),
                "timestamp": time.time()
            }
            
            serialized_data = json.dumps(metrics)
            data_length = len(serialized_data)
            
            mem.seek(0)
            mem.write(b'\x01')  # 1 = écriture en cours
            mem.write(serialized_data.encode('utf-8'))
            mem.write(b'\x00' * (MMAP_SIZE - data_length - 1))  # Remplissage du reste
            mem.seek(0)
            mem.write(b'\x02')  # 2 = écriture terminée
            mem.flush()
            
            time.sleep(UPDATE_INTERVAL)
        
        mem.close()
        
if __name__ == "__main__":
    gpu_available = init_nvml()
    should_stop = Event()
    try:
        collect_and_write_metrics()
    except KeyboardInterrupt:
        print("Arrêt demandé par l'utilisateur.")
    finally:
        if gpu_available:
            pynvml.nvmlShutdown()
        print("Programme arrêté proprement.")
