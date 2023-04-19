import RPi.GPIO as GPIO
import time

def shake(agitator_pin, shakes):
   counter = 0
   while counter < int(shakes):
      GPIO.output(agitator_pin, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(agitator_pin, GPIO.LOW)
      counter += 1
      time.sleep(1)
   print("Agitation finished")
