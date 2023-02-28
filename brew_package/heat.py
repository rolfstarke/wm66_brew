import time
from utils import current_temp
from utils import heater_control

def heat(heater_pin, relay_interval):
    heating_temp = float(input("target temperature?"))
    while current_temp() < heating_temp:
        heater_control(heating_temp, heater_pin, relay_interval)
        time.sleep(relay_interval)
    print("target temperature reached")