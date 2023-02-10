# Script fürs Datalogging und Anzeigen der Temperatur einfügen

import time
from utils import sendMsg
from utils import current_temp
from utils import writeInflux

def cool(relay_interval, measurement_name): 
    cooling_temp = float(input("deploy wort cooler and input target temperature."))
    sendMsg("Jetzt wird abgekuehlt!")
    while current_temp() < cooling_temp:
        time.sleep(relay_interval)
        writeInflux(current_temp(), cooling_temp, measurement_name)
    print("target temperature reached")
    sendMsg("Wuerze auf " + str(cooling_temp) + " Grad gekuehlt. Schmecken lassen!")