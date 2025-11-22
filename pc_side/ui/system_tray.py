import pystray
from pystray import MenuItem, Menu
from PIL import Image
import sys

class SystemTray:
    def __init__(self, app):
        self.app = app
        self.tray = app.tray
        self.tray.set_icon("color/green.jpg")
        self.icon = pystray.Icon(
            "system_monitor",
            Image.open("color/red.jpg"),
            "Micro-bit-PC-monitoring",
            self.create_menu()
        )
    
    def create_menu(self): 
        menu = Menu(
            MenuItem("Quitter", self.quit_action)
        )
        return menu
    def quit_action(self):
        self.icon.stop()
        sys.exit()