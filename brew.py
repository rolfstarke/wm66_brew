
#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import datetime
import RPi.GPIO as GPIO
import keyboard
from w1thermsensor import W1ThermSensor
from influxdb import client as influxdb
from pytz import timezone
#eventuell den pfad zur bot_send.py einfuegen
#import sys
#sys.path.append('hier pfad')
import bot_send

beer_name = input("Ey Fucker, wie heißt das Gesöff? ") + " " + str(datetime.date.today())
bot_send.sendMsg("Guten Tag! Wir brauen heute " + beer_name)
mash_rest_nr = int(input("Wieviele Rasten? "))
mash_rest_times = {}
mash_rest_temp = {}
current_temp = 0 #brauchen wir das noch?
relay_interval = 1
current_mash_timer = 0
agitator_pin =  13            
heater_pin = 11   
rest_reminder = False

#damit nicht die letzten 2 minuten der rast alle sekunde eine nachricht kommt
current_temp = W1ThermSensor().get_temperature() #und das?


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(heater_pin, GPIO.OUT)
GPIO.setup(agitator_pin, GPIO.OUT)
GPIO.output(heater_pin, GPIO.LOW)
GPIO.output(agitator_pin, GPIO.LOW)

# input prompt fuer die zeit und temperatur in ein dict

for i in range(mash_rest_nr):
    mash_rest_times[i] = int(input("Wieviele Minuten fuer Rast Nr. "+str(i+1)+"? ")) * 60
    mash_rest_temp[i] = float(input("Rast Nr. "+str(i+1)+ " auf welcher Temperatur? ")) 

def current_temp():

	temperature = W1ThermSensor().get_temperature()
	return temperature



#influxdb schreiben

def writeInflux(temp, target):
	influxMetric = [{
		'measurement': beer_name,
		'time': datetime.datetime.now(timezone('CET')),
		'fields': {'temperature': temp, 'target_temperature': target}
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
		GPIO.output(heater_pin, GPIO.HIGH)
		time.sleep(relay_interval)
		print("[" + str(datetime.datetime.now(timezone('CET'))) + "]" + " | current temperature: " + str(round(current_temp(), 1)) + " °C " + "| heater: on    ", end='\r')
		writeInflux(current_temp(), target_temp)
	else:
		GPIO.output(heater_pin, GPIO.LOW)
		time.sleep(relay_interval)
		print("[" + str(datetime.datetime.now(timezone('CET'))) + "]" + " | current temperature: " + str(round(current_temp(), 1)) + " °C " + "| heater: idle    ", end='\r')
		writeInflux(current_temp(), target_temp)

# durchgehen der Rasten

input("Press Enter to continue... ")
bot_send.sendMsg("Brauen gestartet, wenn das mal gut geht...")

GPIO.output(agitator_pin, GPIO.HIGH)	# Ruehrwerk starten
try:
	for i in range(mash_rest_nr):
		while current_temp() < mash_rest_temp[i]:
			heater_control(mash_rest_temp[i])
		print("heatup to mash rest " + str(i+1) +" completed")
		bot_send.sendMsg("Rasttemperatur Nr." + str(i+1) + " erreicht.")
		rest_reminder = False
		localtime = time.time()
		endtime = time.time() + mash_rest_times[i] 
		while localtime < endtime:
			heater_control(mash_rest_temp[i])
			localtime = time.time()
			if endtime-localtime <= 120 and rest_reminder == False:
				bot_send.sendMsg("Rast Nr." + str(i+1) + " in 2 Min. fertig.")
				rest_reminder = True
		print("mash rest " + str(i+1) +" completed")
		bot_send.sendMsg("Rast Nr." + str(i+1) + " fertig.")
		current_mash_timer = 0
	print ("last mash completed, Prost!")
	bot_send.sendMsg("Letzte Rast fertig, ihr Schwerenoeter. Schmecken lassen!")
except KeyboardInterrupt:
	GPIO.output(heater_pin, GPIO.LOW)
	GPIO.output(agitator_pin, GPIO.LOW)
	print("Hau ab!")
	bot_send.sendMsg("Brauvorgang abgebrochen, ihr Halunken!")
	pass




GPIO.output(heater_pin, GPIO.LOW)
GPIO.output(agitator_pin, GPIO.LOW)



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
