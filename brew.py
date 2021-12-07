
#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import datetime
import RPi.GPIO as GPIO
import keyboard
from w1thermsensor import W1ThermSensor
from influxdb import client as influxdb
from pytz import timezone

mash_rest_nr = input("Ey Fucker, wieviele Rasten? ")
mash_rest_times = {}
mash_rest_temp = {}
current_temp = 0
relay_interval = 5
current_mash_timer = 0
agitator_pin =  13            
heater_pin = 11             
current_temp = W1ThermSensor().get_temperature()
beer_name = input("Wie heißt das Gesöff?") + str(datetime.date.now(timezone('CET')))

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(heater_pin, GPIO.OUT)
GPIO.setup(agitator_pin, GPIO.OUT)
GPIO.output(heater_pin, GPIO.HIGH)
GPIO.output(agitator_pin, GPIO.HIGH)

# input prompt fuer die zeit und temperatur in ein dict

for i in range(mash_rest_nr):
    mash_rest_times[i] = int(input("Wieviele Minuten fuer Rast Nr. "+str(i+1)+"? ")) * 60
    mash_rest_temp[i] = float(input("Rast Nr. "+str(i+1)+ " auf welcher Temperatur? ")) 

def current_temp():

	temperature = W1ThermSensor().get_temperature()
	return temperature



#influxdb schreiben

def writeInflux(temp):
	influxMetric = [{
		'measurement': beer_name,
		'time': datetime.datetime.now(timezone('CET')),
		'fields': {'temperature': temp}
	}]

	influxHost = 'localhost'
	influxPort = '8086'
	influxUser = 'grafana'
	influxPasswd = 'ERZ2022WM66'
	influxdbName = 'brew_temperature'

	try:
		db = influxdb.InfluxDBClient(influxHost, influxPort, influxUser, influxPasswd, influxdbName)
		db.write_points(influxMetric)
	finally:
		db.close()


# heizungssteuerung

def heater_control(target_temp):
	
	if current_temp() < target_temp :
		GPIO.output(heater_pin, GPIO.LOW)
		time.sleep(relay_interval)
		print("current temperature: " + str(current_temp()) + " heater: on")
		writeInflux(current_temp())
		abort()
	else:
		GPIO.output(heater_pin, GPIO.HIGH)
		time.sleep(relay_interval)
		print("current temperature: " + str(current_temp()) + " heater: idle")
		writeInflux(current_temp())
		abort()

# durchgehen der Rasten

raw_input("Press Enter to continue... ")

GPIO.output(agitator_pin, GPIO.LOW)	# Ruehrwerk starten
try:
	for i in range(mash_rest_nr):
		while current_temp() < mash_rest_temp[i]:
			heater_control(mash_rest_temp[i])
		print("heatup to mash rest" + str(i+1) +" completed")
		localtime = time.time()
		endtime = time.time() + mash_rest_times[i] 
		while localtime < endtime:
			heater_control(mash_rest_temp[i])
			localtime = time.time()
		print("mash rest" + str(i+1) +" completed")
		current_mash_timer = 0
except KeyboardInterrupt:
	print("Was soll ich hier schreiben?")
	GPIO.output(heater_pin, GPIO.HIGH)
	GPIO.output(agitator_pin, GPIO.HIGH)
	pass




GPIO.output(heater_pin, GPIO.HIGH)
GPIO.output(agitator_pin, GPIO.HIGH)
print ("last mash completed, PROST")


# abbruchfunktion

"""def abort():
	while True:
		if keyboard.read_key() == "q":
			GPIO.output(heater_pim, GPIO.HIGH)
			GPIO.output(agitator_pim, GPIO.HIGH)
			mash_rest_times = {}
			mash_rest_temp = {}
			current_temp = 0
			current_mash_timer = 0
			print("ende gelaende")
			break"""
