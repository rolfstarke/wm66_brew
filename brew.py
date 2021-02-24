
#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

mash_rest_nr = input("Ey Fucker, wieviele Rasten?")
mash_rest_times = {}
mash_rest_temp = {}
current_temp = W1ThermSensor().get_temperature()
relay_interval = 1
current_mash_timer = 0
#agitator_pin =              
heater_pin = 11             

GPIO.setmode(GPIO.BOARD)
GPIO.setup(heater_pin, GPIO.OUT)
GPIO.output(heater_pin, GPIO.LOW)

# input prompt fuer die zeit und temperatur in ein dict

for i in range(mash_rest_nr):
    mash_rest_times[i] = int(input("Wieviele Minuten fuer Rast Nr. "+str(i+1)+"?")) * 60
    mash_rest_temp[i] = float(input("Rast Nr. "+str(i+1)+ " auf welcher Temperatur?")) 

# heizungssteuerung

def heater_control(target_temp):
	if current_temp < target_temp :
		GPIO.output(heater_pin, GPIO.LOW)
		time.sleep(relay_interval)
		current_temp = W1ThermSensor().get_temperature()
		print(current_temp + "A")
	else:
		GPIO.output(heater_pin, GPIO.HIGH)
		time.sleep(relay_interval)
		current_temp = W1ThermSensor().get_temperature()
		print(current_temp + "B")

# durchgehen der Rasten

for i in range(mash_rest_nr):
	while current_temp < mash_rest_temp[i]:
		heater_control(mash_rest_temp[i])
	print("heatup to mash rest" + i +" completed") 
	while current_mash_timer < mash_rest_time[i]:
		heater_control(mash_rest_temp[i])
		current_mash_timer += relay_interval
	print("mash rest" + i +" completed")
	current_mash_timer = 0

GPIO.output(heater_pin, GPIO.HIGH)
print ("last mash completed")
