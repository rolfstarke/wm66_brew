
#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

mash_rest_nr = input("Ey Fucker, wieviele Rasten?")
mash_rest_times = {}
mash_rest_temp = {}
current_temp = W1ThermSensor.get_temperature()
relay_interval = 10
current_mash_timer = 0
#agitator_pin =              
heater_pin = 11             

GPIO.setmode(GPIO.BOARD)
GPIO.setup(heatr_pin, GPIO.OUT)

# input prompt fuer die zeit und temperatur in ein dict

for i in range(mash_rest_nr):
    mash_rest_time[i] = int(input("Wieviele Minuten fuer Rast Nr."+i+"?")) * 60
    mash_rest_temp[i] = float(input("Rast Nr."+i+ " auf welcher Temperatur?")) 

# heizungssteuerung

def heater_control(target_temp)
	if current_temp < target_temp :
		GPIO.output(heater_pin, GPIO.LOW)
	else:
		GPIO.output(heater_pin, GPIO.HIGH)

# durchgehen der Rasten

for i in range(mash_rest_nr)
	while current_temp < mash_rest_temp[i]:
		heater_control(mash_rest_temp[i])
		sleep(relay_inerval)
	print("heatup to mash rest" + i +" completed") 
	while current_mash_timer < mash_rest_time[i]:
		heater_control(mash_rest_temp[i])
		sleep(relay_inerval)
		current_mash_timer += relay_interval
	print("mash rest" + i +" completed")
	current_mash_timer = 0

GPIO.output(heater_pin, GPIO.HIGH)
print ("last mash completed")
