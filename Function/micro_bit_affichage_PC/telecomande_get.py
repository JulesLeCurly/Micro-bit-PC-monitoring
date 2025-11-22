import serial
import pyautogui
import time

#  Trouver automatiquement le port série de la micro:bit
import serial.tools.list_ports

PORT = 'COM3'
BAUDRATE = 115200

if PORT is None:
    print(" Micro:bit non détectée. Vérifiez la connexion USB.")
    exit()

#  Paramètres d'écran
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
X_CENTER = SCREEN_WIDTH // 2
Y_CENTER = SCREEN_HEIGHT // 2

#  Sensibilité des mouvements (facteur de mise à l'échelle)
SENSITIVITY = 4  # Ajustez cette valeur selon vos préférences

#  Variables d'initialisation
X_init = None
Y_init = None

try:
    # Ouvrir la connexion série
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f" Connexion ouverte sur {PORT}")

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                x, y, z = map(int, line.split(","))
                x = -x
                y = z

                # Initialisation des valeurs de référence
                if X_init is None:
                    X_init = x
                    Y_init = y
                    print(" Réglage initial des valeurs de référence")
                    new_x = X_CENTER
                    new_y = Y_CENTER

                # Calcul du déplacement avec normalisation
                dx = (x - X_init) * SENSITIVITY
                dy = (y - Y_init) * SENSITIVITY

                # Déterminer la nouvelle position de la souris
                new_x = ((X_CENTER + dx) + new_x*3) / 4
                new_y = ((Y_CENTER - dy) + new_y*3) / 4# Inversion de Y pour un déplacement intuitif

                # Contrainte pour ne pas sortir de l'écran
                new_x = max(0, min(SCREEN_WIDTH, new_x))
                new_y = max(0, min(SCREEN_HEIGHT, new_y))

                # Déplacement de la souris
                pyautogui.moveTo(new_x, new_y, duration=0.05)  # Mouvement fluide
                
                print(f" Déplacement souris - X: {new_x}, Y: {new_y}")
            except ValueError:
                print(f" Erreur de conversion : {line}")

except serial.SerialException as e:
    print(f" Impossible d'ouvrir le port série : {e}")
except KeyboardInterrupt:
    print(" Arrêt du programme.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Connexion série fermée.")
