import serial
import serial.tools.list_ports
import psutil
import time
from py3nvml import py3nvml as nvml
import threading
import pystray
from pystray import MenuItem, Menu
from PIL import Image

device_port = "COM3"  # choisissez votre port évidemment

nvml.nvmlInit()
device_count = nvml.nvmlDeviceGetCount()
handle = nvml.nvmlDeviceGetHandleByIndex(0)


running = True

def wait_for_start():
    try:
        arduinoData = serial.Serial(device_port, 115200)
        while running:
            if arduinoData.in_waiting > 0:
                message = arduinoData.readline().decode().strip()
                if message == "START":
                    collect_data(arduinoData)
                    break
    except serial.serialutil.SerialException:
        time.sleep(1)
        if running:
            wait_for_start()

def disconnected():
    icon.icon = Image.open("logoCPU-disconnected.ico")
    wait_for_start()

def collect_data(arduinoData):
    icon.icon = Image.open("logoCPU-connected.ico")
    try:
        while running:
            GPU_temp = nvml.nvmlDeviceGetTemperature(handle, nvml.NVML_TEMPERATURE_GPU)
            GPU_usage = nvml.nvmlDeviceGetUtilizationRates(handle).gpu
            CPU_usage = int(psutil.cpu_percent(interval=0, percpu=False) * 5)
            RAM_usage = int(psutil.virtual_memory().percent)
            Disk_usage = int(psutil.disk_usage("C:\\").percent)

            if CPU_usage > 100:
                CPU_usage = 100
            CPU_value = int(160 - 1.6 * CPU_usage)
            GPU_usage_value = int(160 - 1.6 * GPU_usage)
            Disk_value = int(160 - 1.6 * Disk_usage)
            RAM_value = int(160 - 1.6 * RAM_usage)
            GPU_temp_value = int(160 - 1.6 * GPU_temp)

            data = f"{CPU_value};{GPU_usage_value};{RAM_value};{Disk_value};{GPU_temp_value}\r"
            arduinoData.write(data.encode())
            time.sleep(1)
    except serial.serialutil.SerialException:
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

icon = pystray.Icon("system_monitor", Image.open("logoCPU-disconnected.ico"), "UtilShower (by Ypsol)", create_menu())

data_thread = threading.Thread(target=wait_for_start, daemon=True)
data_thread.start()

icon.run()
