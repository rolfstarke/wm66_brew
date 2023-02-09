
import RPi.GPIO as GPIO
import argparse
import keyboard

from brew_package.testfunction import printtime
from brew_package.agitate import
from brew_package.bot_listen import
from brew_package.bot_send import
from brew_package.cool import
from brew_package.wort import
from brew_package.mash import
from brew_package.heat import


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

printtime()