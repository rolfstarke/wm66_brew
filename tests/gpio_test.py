import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

try:
  while True:
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
except KeyboardInterrupt:
    GPIO.output(13, GPIO.HIGH)  
    GPIO.output(11, GPIO.LOW)
    print("abgebrochen, fucker")
