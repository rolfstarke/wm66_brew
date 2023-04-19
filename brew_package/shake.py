
import RPi.GPIO as GPIO
import time

def shake(agitator_pin):
   
    GPIO.output(agitator_pin, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(agitator_pin, GPIO.LOW)
    print("agitation finished")
