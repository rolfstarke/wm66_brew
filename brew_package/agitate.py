
import RPi.GPIO as GPIO
import time

def agitate(agitator_pin):
    agitation_time = float(input("minutes to agitate for? ")) * 60
    GPIO.output(agitator_pin, GPIO.HIGH)
    time.sleep(agitation_time)
    GPIO.output(agitator_pin, GPIO.LOW)
    print("agitation finished")