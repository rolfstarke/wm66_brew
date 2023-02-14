# anpassen ans würzekochen

import time
import RPi.GPIO as GPIO
from utils import current_temp
from utils import heater_control
from utils import sendMsg
from utils import writeInflux


class xhopping:
    '''object that stores its number, the time, and the message status for a hopping'''

    def __init__(self, order):
        self.number = order
        self.time = int(
            input("Hopfengabe " + str(self.number)+" bei wieviel Minuten? ")) * 60
        self.noticed = False
        self.instructed = False


def wort(agitator_pin, heater_pin, relay_interval, measurement_name):
	hoppings = []
	wort_time = int(input("Wieviele Minuten soll die Wuerze gekocht werden? ")) * 60
	tmp = int(input("Wieviele Hopfengaben? "))
	GPIO.output(agitator_pin, GPIO.HIGH)  # Ruehrwerk starten
	for i in range(tmp):
		hoppings.append(xhopping(i+1))
		while current_temp() < 95:
			heater_control(98, heater_pin, relay_interval)
			writeInflux(current_temp(), 98, measurement_name)
		print("starting wort")
		sendMsg("Wuerzekochen!")
		localtime = time.time()
		endtime = time.time() + wort_time
		while localtime < endtime:
			heater_control(98, heater_pin, relay_interval)
			writeInflux(current_temp(), 98)
			localtime = time.time()
			for i in range(hoppings):
				if 1 <= endtime-localtime-hoppings[i].time <= 120 and hoppings[i].noticed == False:
					sendMsg("Hopfengabe" + hoppings[i].number + " in 2 Minuten")
					hoppings[i].noticed = True
					if endtime-localtime-hoppings[i].time <= 0 and hoppings[i].instructed == False:
						sendMsg("Hopfengabe! Hopfengabe Nr" + hoppings[i].number + "! ZackZack")
					hoppings[i].instructed = True
	print("wort completed")
	sendMsg("Wuerzekochen abgeschlossen")
	GPIO.output(heater_pin, GPIO.LOW)
	GPIO.output(agitator_pin, GPIO.LOW)
