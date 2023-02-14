from w1thermsensor import W1ThermSensor
from influxdb import client as influxdb
import RPi.GPIO as GPIO
from pytz import timezone
import datetime
import time
import requests

# Temperatur abfragen


def current_temp():

    temperature = W1ThermSensor().get_temperature()
    return temperature

# influxdb schreiben


def writeInflux(temperature, target_temperature, measurement_name):
    influxMetric = [{
        'measurement': measurement_name,
        'time': datetime.datetime.now(timezone('CET')),
        'fields': {'temperature': temperature, 'target_temperature': target_temperature}
    }]

    influxHost = 'localhost'
    influxPort = '8086'
    influxUser = 'grafana'
    influxPasswd = 'ERZ2022WM66'
    influxdbName = 'brew_temperature'

    try:
        db = influxdb.InfluxDBClient(
            influxHost, influxPort, influxUser, influxPasswd, influxdbName)
        db.write_points(influxMetric)
    finally:
        db.close()

# heizungssteuerung


def heater_control(target_temp, heater_pin, relay_interval):

    if current_temp() < target_temp:
        GPIO.output(heater_pin, GPIO.HIGH)
        print("[" + str(datetime.datetime.now(timezone('CET'))) + "]" + " | current temperature: " +
              str(round(current_temp(), 1)) + " °C " + "| heater: on    ", end='\r')
        time.sleep(relay_interval)
    else:
        GPIO.output(heater_pin, GPIO.LOW)
        print("[" + str(datetime.datetime.now(timezone('CET'))) + "]" + " | current temperature: " +
              str(round(current_temp(), 1)) + " °C " + "| heater: idle    ", end='\r')
        time.sleep(relay_interval)

# bot nachrichten senden

def sendMsg(msg):
    #Pfad zum Token einfügen    
    with open("data/token.txt") as file:
        token = file.read().splitlines()
    url = f"https://api.telegram.org/bot{token[0]}/sendMessage"
    params = {"chat_id":"-792733418", "text":msg}
    message = requests.post(url, params=params)
