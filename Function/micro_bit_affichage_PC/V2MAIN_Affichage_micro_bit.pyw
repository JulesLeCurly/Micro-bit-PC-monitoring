import serial
import serial.tools.list_ports
import time
import threading
import pystray
from pystray import MenuItem, Menu
from PIL import Image
import sys

import Fonction.ON_PC as ON_PC


# Port série du micro:bit (remplacez par votre port)
microbit_port = 'COM14'  # Windows : COMx ; macOS/Linux : /dev/ttyACMx
baud_rate = 115200  # Doit correspondre au paramètre côté micro:bit

# Envoyer des données au micro:bit
running = True



class Microbit_communication:
    def __init__(self):
        self.UPDATE_INTERVAL = 0.25
        self.microbit_port = microbit_port
        self.baud_rate = baud_rate
        self.serial_port = None
        self.running_ALL = True
        self.mode = "OFF"

        print("running")
    
    def connected(self):
        icon.icon = Image.open("color/green.jpg")
    
    def disconnected(self):
        icon.icon = Image.open("color/red.jpg")
    

    def get_actual_mode(self):
        ON_pc = False
        Telcomande = False
        try:
            serial.Serial(microbit_port, baud_rate, timeout=1)
            ON_pc = True
            self.mode = "ON_PC"
        except:
            ON_pc = False
        if ON_pc == False:
            try:
                Telcomande = True
                self.mode = "Telcomande"
            except:
                Telcomande = False
        
        if ON_pc == False and Telcomande == False:
            self.mode = "OFF"
        return self.mode
    
    def wait_for_start(self):
        mode = self.get_actual_mode()
        if mode == "OFF":
            self.disconnected()
            time.sleep(1)
            self.wait_for_start()
        elif mode == "ON_PC":
            self.connected()
        elif mode == "Telcomande":
            self.connected()
    
    def main(self):
        self.wait_for_start()
        while self.running_ALL:
            print(time.time(), self.mode)
            if self.mode == "ON_PC":
                running = True
                try:
                    with serial.Serial(microbit_port, baud_rate, timeout=1) as ser:
                        while running:
                            ser.write(ON_PC.main())
                            time.sleep(self.UPDATE_INTERVAL)
                except:
                    time.sleep(2) # Wait if the probleme can be fixed itself
                    self.wait_for_start()
            elif self.mode == "Telcomande":
                pass
            elif self.mode == "OFF":
                time.sleep(1)
                self.wait_for_start()
            else:
                time.sleep(2) # Wait if the probleme can be fixed itself
                self.wait_for_start()


def quit_action():
    global icon
    icon.stop()
    sys.exit()

def create_menu(): 
    menu = Menu(
        MenuItem("Quitter", quit_action)
    )
    return menu

icon = pystray.Icon("system_monitor", Image.open("color/red.jpg"), "CPU/GPU/MEM Live ;)", create_menu())

microbit_communication = Microbit_communication()

data_thread = threading.Thread(target=microbit_communication.main(), daemon=True)
data_thread.start()

icon.run()