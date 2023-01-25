

import time
import datetime
import RPi.GPIO as GPIO
import keyboard
from w1thermsensor import W1ThermSensor
from influxdb import client as influxdb
from pytz import timezone
import bot_send  # eventuell den pfad zur bot_send.py einfuegen
import argparse

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(heater_pin, GPIO.OUT)
GPIO.setup(agitator_pin, GPIO.OUT)
GPIO.output(heater_pin, GPIO.LOW)
GPIO.output(agitator_pin, GPIO.LOW)

# create an ArgumentParser object and a mutually exclusive group. add command line arguments and parse the arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-c", "--cool", help="Abkuehlen - Heizung und Ruehrwerk sind aus, es wird nur die Temperatur geloggt", action='store_true')
group.add_argument("-w", "--wort", help="Wuerzekochen", action='store_true')
group.add_argument("-m", "--mash", help="Maischen", action='store_true')
group.add_argument("--heat", help="Heizen", action='store_true')
group.add_argument("--agitate", help="Ruehren", action='store_true')
args = parser.parse_args()

relay_interval = 5
agitator_pin = 13
heater_pin = 11
rest_reminder = False
hoppings = []
# Temperatur abfragen


def current_temp():

    temperature = W1ThermSensor().get_temperature()
    return temperature

# influxdb schreiben


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
        db = influxdb.InfluxDBClient(
            influxHost, influxPort, influxUser, influxPasswd, influxdbName)
        db.write_points(influxMetric)
    finally:
        db.close()

# heizungssteuerung


def heater_control(target_temp):

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

# die Klasse Hopfengaben


class xhopping:
    '''object that stores its number, the time, and the message status for a hopping'''

    def __init__(self, order):
        self.number = order
        self.time = int(
            input("Hopfengabe " + str(self.number)+" bei wieviel Minuten? ")) * 60
        self.notice = False
        self.instruction = False


try:
    if args.heat:
        heating_temp = float(input("target temperature?"))
        while current_temp() < heating_temp:
            heater_control(heating_temp)
            time.sleep(relay_interval)
        print("target temperature reached")
    elif args.agitate:
        agitation_time = int(input("minutes to agitate for? ") * 60)
        GPIO.output(agitator_pin, GPIO.HIGH)
        time.sleep(agitation_time)
        GPIO.output(agitator_pin, GPIO.LOW)
        print("agitation finished")

    beer_name = input("Ey Fucker, wie heißt das Gesoeff? ") + \
        " " + str(datetime.date.today())

    if args.cool:
        cooling_temp = float(
            input("deploy wort cooler and input target temperature."))
        bot_send.sendMsg("Wuerzekuehlung begonnen.")
        while current_temp() < cooling_temp:
            time.sleep(relay_interval)
            writeInflux(current_temp(), cooling_temp)
        print("target temperature reached")
        bot_send.sendMsg("Wuerze auf " + str(cooling_temp) + " Grad gekuehlt.")
    elif args.wort:
        wort_time = int(
            input("Wieviele Minuten soll die Wuerze gekocht werden "+str(i+1)+"? ")) * 60
        tmp = int(input("Wieviele Hopfengaben? "))
        for i in tmp:
            hoppings.append(xhopping(i+1))
        GPIO.output(agitator_pin, GPIO.HIGH)  # Ruehrwerk starten
        while current_temp() < 95:
            heater_control(98)
            writeInflux(current_temp(), 98)
        print("starting wort")
        bot_send.sendMsg("Wuerzekochen beginnt")
        localtime = time.time()
        endtime = time.time() + wort_time
        while localtime < endtime:
            heater_control(98)
            writeInflux(current_temp(), 98)
            localtime = time.time()
            for i in range(hoppings):
                if 1 <= endtime-localtime-hoppings[i].time <= 120 and hoppings[i].notice == False:
                    bot_send.sendMsg(
                        "Hopfengabe" + hoppings[i].number + " in 2 Minuten")
                    hoppings[i].notice = True
                    if endtime-localtime-hoppings[i].time <= 0 and hoppings[i].instruction == False:
                        bot_send.sendMsg("Hopfengabe! Hopfengabe Nr" +
                                         hoppings[i].number + "! ZackZack")
                    hoppings[i].instruction = True
        print("wort completed")
        bot_send.sendMsg("Wuerzekochen abgeschlossen")
    elif args.mash:
        bot_send.sendMsg("Guten Tag! Wir brauen heute " + beer_name)
        mash_rest_nr = int(input("Wieviele Rasten? "))
        mash_rest_times = {}
        mash_rest_temp = {}
        for i in range(mash_rest_nr):
            mash_rest_times[i] = int(
                input("Wieviele Minuten fuer Rast Nr. "+str(i+1)+"? ")) * 60
            mash_rest_temp[i] = float(
                input("Rast Nr. "+str(i+1) + " auf welcher Temperatur? "))
        input("Press Enter to continue... ")
        bot_send.sendMsg("Brauen gestartet, wenn das mal gut geht...")
        GPIO.output(agitator_pin, GPIO.HIGH)  # Ruehrwerk starten
        for i in range(mash_rest_nr):
            while current_temp() < mash_rest_temp[i]:
                heater_control(mash_rest_temp[i])
                writeInflux(current_temp(), mash_rest_temp[i])
            print("heatup to mash rest " + str(i+1) + " completed")
            bot_send.sendMsg("Rasttemperatur Nr." + str(i+1) + " erreicht.")
            rest_reminder = False
            localtime = time.time()
            endtime = time.time() + mash_rest_times[i]
            while localtime < endtime:
                heater_control(mash_rest_temp[i])
                writeInflux(current_temp(), mash_rest_temp[i])
                localtime = time.time()
                if endtime-localtime <= 120 and rest_reminder == False:
                    bot_send.sendMsg("Rast Nr." + str(i+1) +
                                     " in 2 Min. fertig.")
                    rest_reminder = True
            print("mash rest " + str(i+1) + " completed")
            bot_send.sendMsg("Rast Nr." + str(i+1) + " fertig.")
        print("last mash completed, Prost!")
        bot_send.sendMsg(
            "Letzte Rast fertig, ihr Schwerenoeter. Schmecken lassen!")
except KeyboardInterrupt:
    GPIO.output(heater_pin, GPIO.LOW)
    GPIO.output(agitator_pin, GPIO.LOW)
    print("Hau ab!")
    bot_send.sendMsg("Brauvorgang abgebrochen, ihr Halunken!")
    pass

GPIO.output(heater_pin, GPIO.LOW)
GPIO.output(agitator_pin, GPIO.LOW)
