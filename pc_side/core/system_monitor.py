import pynvml
import psutil

class SystemMonitor:
    def __init__(self):
        self.gpu_available = self.init_nvml()
    
    def init_nvml(self):
        """Initialisation de NVML avec gestion des erreurs."""
        try:
            pynvml.nvmlInit()
            return True
        except pynvml.NVMLError as e:
            print(f"Erreur NVML : {e}")
            return False

    def get_gpu_metrics(self):
        """Récupère l'utilisation et la température du GPU si disponible."""
        if not self.gpu_available:
            return {"error": "GPU not available"}
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            Vram = pynvml.nvmlDeviceGetMemoryInfo(handle)
            fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
            return {"usage": util.gpu, "temperature": temp, "vram": Vram.used, "fan_speed": fan_speed}
        except pynvml.NVMLError as e:
            return {"error": str(e)}
    
    def get_cpu_usage(self):
        """Récupère l'utilisation du CPU."""
        return {"usage": psutil.cpu_percent()}

    def get_memory_usage(self):
        """Récupère l'utilisation de la mémoire."""
        return {"usage": psutil.virtual_memory().percent}