
import RPi.GPIO as GPIO
import time

def agitate(agitator_pin):
    agitation_time = int(input("minutes to agitate for? "))
    print(agitation_time * 60)
    GPIO.output(agitator_pin, GPIO.HIGH)
    time.sleep(agitation_time * 60)
    GPIO.output(agitator_pin, GPIO.LOW)
    print("agitation finished")