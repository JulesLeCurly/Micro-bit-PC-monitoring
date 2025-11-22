import subprocess
import screeninfo

def get_screen_count():
    """Retourne le nombre d'écrans actuellement connectés."""
    screens = screeninfo.get_monitors()
    return len(screens)

def toggle_second_screen():
    """Active ou désactive le deuxième écran en fonction de son état actuel."""
    if get_screen_count() > 1:
        print("Désactivation du deuxième écran...")
        subprocess.run(["C:\\Windows\\System32\\DisplaySwitch.exe", "/internal"])
    else:
        print("Activation du deuxième écran...")
        subprocess.run(["C:\\Windows\\System32\\DisplaySwitch.exe", "/extend"])
