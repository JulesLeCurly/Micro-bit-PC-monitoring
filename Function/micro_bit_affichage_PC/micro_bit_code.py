from microbit import *

# Initialiser la communication UART sur les broches par défaut (USB)
uart.init(baudrate=115200)
display.show(Image('90309:'
                   '03630:'
                   '36963:'
                   '03630:'
                   '90309'))

def liste_to_massage(screen_liste):
    message = ""
    for y in range(0, 5):
        for x in range(0, 5):
            message += str(round( (screen_liste[x][y] * 9) / 100) )
        if y != 4:
            message += ":"
    return message


def prc_in_list(prc):
    # Limitation du pourcentage entre 0 et 100
    prc = max(0, min(prc, 100))
    
    # Calcul du nombre de LEDs allumées
    nb_led_on = (prc * 5) / 100
    
    # Calcul de la luminosité de la LED partiellement allumée
    color_of_the_rest = round((nb_led_on - int(nb_led_on)) * 100)
    
    # Nombre de LEDs partiellement allumées (0 ou 1)
    nb_led_of_the_rest = 1 if color_of_the_rest > 0 else 0
    
    # Nombre de LEDs éteintes
    nb_led_off = 5 - int(nb_led_on) - nb_led_of_the_rest
    
    list_led_on = [100] * int(nb_led_on)
    list_led_of_the_rest = [color_of_the_rest] * nb_led_of_the_rest
    list_led_off = [0] * nb_led_off
    
    # Construction des listes
    list_led = []
    for ellement in list_led_on:
        list_led.append(ellement)
    for ellement in list_led_of_the_rest:
        list_led.append(ellement)
    for ellement in list_led_off:
        list_led.append(ellement)
    
    #list_led = list(reversed(list_led))

    return list_led

def temperature_transformation(temperature_prc):
    max = 30
    min = 20

    temperature_final = (temperature_prc - min) * 100 / (max - min)

    return temperature_final

while True:
    if uart.any():
        data = uart.read()
        if data:
            temperature_prc = temperature()
            temperature_prc = temperature_transformation(temperature_prc)

            data = str(data, 'utf-8')

            data = data.split(":")
            cpu_prc = float(data[0])
            mem_prc = float(data[1])
            gpu_prc = float(data[2])
            temp_prc = float(temperature_prc)
            global_prc = (cpu_prc + mem_prc + gpu_prc) / 3

            cpu_prc_list = prc_in_list(cpu_prc)
            mem_prc_list = prc_in_list(mem_prc)
            gpu_prc_list = prc_in_list(gpu_prc)
            temp_prc_list = prc_in_list(temp_prc)
            global_prc_list = prc_in_list(global_prc)

            screen_liste = [
                cpu_prc_list,
                mem_prc_list,
                gpu_prc_list,
                temp_prc_list,
                global_prc_list]
            screen_liste = list(reversed(screen_liste))
            screen_data = liste_to_massage(screen_liste)

            screen = Image(screen_data)
            display.show(screen)
            
#https://python.microbit.org/v/3/reference/display