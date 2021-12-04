import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

try:
  while True:
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
except KeyboardInterrupt:
  GPIO.output(11, GPIO.HIGH)  
  GPIO.output(13, GPIO.HIGH)
