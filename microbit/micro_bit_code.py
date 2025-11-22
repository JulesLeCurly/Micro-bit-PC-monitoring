from microbit import *

Busy_image = Image('90309:'
                   '03630:'
                   '36963:'
                   '03630:'
                   '90309')

# ---------------------------------------
# Constants
# ---------------------------------------
Max_temperature = 100
Min_temperature = 0
Baud_rate = 115200

# ---------------------------------------
# UART setup
# ---------------------------------------
# Initialise communication UART on default pins (USB)
uart.init(baudrate=Baud_rate)

# ---------------------------------------
# Function
# ---------------------------------------
def Pourcentage_to_liste(prc):
    # Limit percentage between 0 and 100
    prc = max(0, min(prc, 100))
    
    # Calculate number of lit LEDs
    nb_led_on = (prc * 5) / 100
    
    # Calculate brightness of the partially lit LED
    color_of_the_rest = round((nb_led_on - int(nb_led_on)) * 100)
    
    # Number of partially lit LEDs (0 or 1)
    nb_led_of_the_rest = 1 if color_of_the_rest > 0 else 0
    
    # Number of unlit LEDs
    nb_led_off = 5 - int(nb_led_on) - nb_led_of_the_rest
    
    list_led_on = [100] * int(nb_led_on)
    list_led_of_the_rest = [color_of_the_rest] * nb_led_of_the_rest
    list_led_off = [0] * nb_led_off
    
    # Construct lists
    list_led = []
    for ellement in list_led_on:
        list_led.append(ellement)
    for ellement in list_led_of_the_rest:
        list_led.append(ellement)
    for ellement in list_led_off:
        list_led.append(ellement)
    
    return list_led

def Temperature_transformation(temperature_prc):
    return (temperature_prc - Min_temperature) * 100 / (Max_temperature - Min_temperature)

def Array_to_Image(screen_array):
    img_str = ""
    for y in range(5):
        for x in range(5):
            brightness = round((screen_array[x][y] * 9) / 100)
            img_str += str(brightness)
        if y != 4:
            img_str += ":"
    return Image(img_str)

# ---------------------------------------
# Main loop
# ---------------------------------------
while True:
    if uart.any():
        data = uart.read()
        if data:
            data = str(data, 'utf-8')

