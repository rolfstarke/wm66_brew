import RPi.GPIO as GPIO
import time

def shake(agitator_pin):
   counter = 0
   shakes = int(input("Wie of wollt ihr Rütteln? Und wehe ihr sperrt mich wieder aus Chatgruppe aus. Bratzen. "))
   while counter < int(shakes):
      GPIO.output(agitator_pin, GPIO.HIGH)
      time.sleep(0.05)
      GPIO.output(agitator_pin, GPIO.LOW)
      counter += 1
      time.sleep(2)
   print("Agitation finished")
