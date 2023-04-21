#!/usr/bin/python3

import keyboard
import time
import subprocess
import datetime
import RPi.GPIO as GPIO
import argparse
from configparser import ConfigParser
from utils import current_temp
from utils import writeInflux
from utils import heater_control
from utils import sendMsg
from brew_package.heat import heat
from brew_package.agitate import agitate
from brew_package.cool import cool
from brew_package.wort import wort
from brew_package.mash import mash
from brew_package.shake import shake

# import brew_package.bot_listen

with open('meta/ascii-humpen.txt', 'r') as file:
    for line in file:
        print(line)
        time.sleep(0.07)

# read all the settings from external config file
config = ConfigParser()
config.read('config.ini')
relay_interval = int(config.get('main', 'relay_interval'))
agitator_pin = int(config.get('main', 'agitator_pin'))
heater_pin = int(config.get('main', 'heater_pin'))

# relay_interval = 5
# agitator_pin = 13
# heater_pin = 11


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(heater_pin, GPIO.OUT)
GPIO.setup(agitator_pin, GPIO.OUT)
GPIO.output(heater_pin, GPIO.LOW)
GPIO.output(agitator_pin, GPIO.LOW)

# create an ArgumentParser object and a mutually exclusive group. add command line arguments and parse the arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--cool", help="Abkuehlen - Heizung und Ruehrwerk sind aus, es wird nur die Temperatur geloggt", action='store_true')
group.add_argument("-w", "-wort", "--wort", help="Wuerzekochen", action='store_true')
group.add_argument("-m", "-mash", "--mash", help="Maischen", action='store_true')
group.add_argument("--heat", help="Heizen", action='store_true')
group.add_argument("--agitate", help="Ruehren", action='store_true')
group.add_argument("--shake", help="Ruetteln", action='store_true')
parser.add_argument("-t", "--telegram", help='Telegrambot starten', action='store_true')
args = parser.parse_args()

# die Klasse Hopfengaben

try:
    if args.telegram:
        sendMsg("Ich hoere zu.")
        # brew_package.bot_listen

    elif args.heat:
        heat(heater_pin, relay_interval)

    elif args.agitate:
        agitate(agitator_pin)
        
    elif args.shake:
        shake(agitator_pin)

    beer_name = input("Ey Fucker, wie heißt das Gesoeff? ") + \
        " " + str(datetime.date.today())

    if args.cool:
        cool(relay_interval, beer_name)

    elif args.wort:
        wort(agitator_pin, heater_pin, relay_interval, beer_name)

    elif args.mash:
        mash(agitator_pin, heater_pin, relay_interval, beer_name)

except KeyboardInterrupt:
    print("Hau ab!")
    sendMsg("Brauvorgang abgebrochen, ihr Halunken!")
    
except Exception as e:
    print(e)
    
finally:
    GPIO.cleanup()
