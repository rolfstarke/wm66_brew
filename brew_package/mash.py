

import time
import RPi.GPIO as GPIO
from utils import current_temp
from utils import heater_control
from utils import sendMsg
from utils import writeInflux


class xrest:
    '''object that stores its number, the time, the temperature and the message status for a mash rest'''

    def __init__(self, order):
        self.number = order
        self.time = float(input("Wieviele Minuten fuer Rast Nr. "+str(self.number)+"? ")) * 60
        self.temperature = float(input("Rast Nr. "+str(self.number)+" auf welcher Temperatur? "))
        self.noticed = False


def mash(agitator_pin, heater_pin, relay_interval, measurement_name):
    mash_rests = []
    sendMsg("Guten Tag! Wir brauen heute " + measurement_name)
    for i in range(int(input("Wieviele Rasten? "))):
        mash_rests.append(xrest(i+1))
    input("Press Enter to continue... ")
    sendMsg("Es wird eingemaischt!")
    GPIO.output(agitator_pin, GPIO.HIGH)  # Ruehrwerk starten
    print(mash_rests)
    for i in range(len(mash_rests)):
        while current_temp() < mash_rests[i].temperature:
            heater_control(mash_rests[i].temperature,
                           heater_pin, relay_interval)
            writeInflux(current_temp(),
                        mash_rests[i].temperature, measurement_name)
        print("heatup to mash rest " + str(i+1) + " completed")
        sendMsg("Rasttemperatur Nr." + str(i+1) + " erreicht.")
        endtime = time.time() + mash_rests[i].time
        while time.time() < endtime:
            heater_control(mash_rests[i].temperature, heater_pin, relay_interval)
            writeInflux(current_temp(), mash_rests[i].temperature, measurement_name)
            if endtime-time.time() <= 120 and mash_rests[i].noticed == False:
                sendMsg("Rast Nr." + str(i+1) +
                        " in 2 Min. fertig.")
                mash_rests[i].noticed = True
        print("mash rest " + str(i+1) + " completed")
        sendMsg("Rast Nr." + str(i+1) + " fertig.")
    print("last mash completed")
    sendMsg("Letzte Rast fertig, ihr Schwerenoeter.")
    GPIO.output(heater_pin, GPIO.LOW)
    GPIO.output(agitator_pin, GPIO.LOW)
